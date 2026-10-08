"""Deterministic regression tests. These do not evaluate an LLM or prove mathematics."""
from __future__ import annotations
import contextlib,io,json,os
from pathlib import Path
import shutil,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'scripts'))
from tex_scan import mask_noncode,inline_math,read_group
from tex_project import expand_project,ProjectError
from check_style import check,locked
from content_style_lint import lint
from tex_guard import scan_text,scan_project
from validation_policy import load_policy,annotate_warnings
from build_utils import sha256,build
from log_audit import audit
from measure_inline import instrument,measure
from artifact_records import verify_records
GOLD=(ROOT/'templates/wangzhe_baiti_style.tex').read_text(encoding='utf-8')
PREFIX=GOLD.split(r'\begin{document}',1)[0]
def doc(body): return PREFIX+'\n\\begin{document}\n\\mainmatter\n\\originalchapter{测试}\n'+body+'\n\\end{document}\n'
def errors(body): return {f.kind for f in lint(doc(body))[0] if f.level=='ERROR'}

class ScanTests(unittest.TestCase):
    def test_comments_offsets(self):
        t='正文% ignored\n'+r'50\% $x$'; s=mask_noncode(t)
        self.assertEqual(len(t),len(s)); self.assertNotIn('ignored',s); self.assertEqual(s.count('\n'),t.count('\n'))
    def test_inline_verb_percent(self):
        s=mask_noncode(r'\verb|% $fake$| $x$'); self.assertEqual([x.content for x in inline_math(s)],['x'])
    def test_multiline_verbatim(self):
        s='\\begin{verbatim}\n\\input{missing}\n$x$\n\\end{verbatim}\n$y$'
        self.assertEqual([x.content for x in inline_math(s)],['y']); self.assertEqual(mask_noncode(s).count('\n'),4)
    def test_escaped_dollar(self): self.assertEqual([x.content for x in inline_math(r'\$2 $x$')],['x'])
    def test_display_not_inline(self): self.assertEqual([x.content for x in inline_math(r'\[x\] $$y$$ \begin{align*}a&=b\end{align*} $z$')],['z'])
    def test_parenthesis(self): self.assertEqual(inline_math(r'\(x+y\)')[0].content,'x+y')
    def test_unclosed(self):
        with self.assertRaises(ValueError): inline_math('$x')
    def test_unclosed_display(self):
        with self.assertRaises(ValueError): inline_math(r'\[x')
    def test_nested_group(self): self.assertEqual(read_group('{a{b}}',0),('a{b}',6))
    def test_literal_command(self): self.assertNotIn(r'\input',mask_noncode(r'\string\input \detokenize{\input{bad}}'))

class LayoutTests(unittest.TestCase):
    def test_template(self): self.assertEqual(check(GOLD),[])
    def test_font_change(self): self.assertTrue(check(GOLD.replace('setstretch{1.6}','setstretch{1.3}')))
    def test_math_macro_allowed(self): self.assertFalse(check(doc(r'\newcommand{\F}{\mathbb F}')))
    def test_function_environment_allowed(self): self.assertFalse(check(doc(r'\newenvironment{myalgorithm}{\begin{enumerate}}{\end{enumerate}}')))
    def test_proof_override(self): self.assertTrue(check(doc(r'\renewenvironment{proof}{}{}')))
    def test_commented_override_ignored(self): self.assertFalse(check(doc('% \\setmainfont{Bad}\n正文')))
    def test_verbatim_override_ignored(self): self.assertFalse(check(doc(r'\verb|\setmainfont{Bad}|')))
    def test_long_title_not_error(self): self.assertFalse(errors(r'\originalsection{这个标题很长但不能据此判定数学内容或讲解质量不合格}'))
    def test_lookup_title_allowed(self): self.assertFalse(errors(r'\originalsection{速查表}'))
    def test_steps_allowed(self): self.assertFalse(errors(r'\textbf{第一步：}构造. \textbf{核心思路：}解释.'))
    def test_work_log_quote_not_blacklisted(self): self.assertFalse(errors('本例说明“本次未找到”属于报告文字.'))
    def test_long_preface_not_capped(self): self.assertFalse(errors(r'\originalpreface '+'文'*650))
    def test_parenthesis_condition_allowed(self): self.assertFalse(errors(r'\begin{exercise}(必要条件) 证明题面中的条件成立.\end{exercise}'))
    def test_minipage_not_box(self): self.assertFalse(errors(r'\begin{minipage}{.5\linewidth}正文.\end{minipage}'))
    def test_graphic_scaling_not_error(self): self.assertFalse(errors(r'\resizebox{3cm}{!}{图片}'))
    def test_proof_end_is_review(self): self.assertFalse(errors(r'\begin{proof}\[a=b.\]\end{proof}'))
    def test_qedhere(self): self.assertFalse(errors(r'\begin{proof}\[a=b.\qedhere\]\end{proof}'))
    def test_dfrac_review(self): self.assertFalse(errors(r'$\dfrac{a}{b}$'))
    def test_smallmatrix(self): self.assertFalse(errors(r'$\left(\begin{smallmatrix}1&0\\0&1\end{smallmatrix}\right)$'))
    def test_empty_proof_error(self): self.assertIn('empty-proof',errors(r'\begin{proof}\end{proof}'))
    def test_mismatched_environment(self): self.assertIn('environment-balance',errors(r'\begin{proof}x\end{solution}'))
    def test_no_proof_quota(self): self.assertFalse(errors(r'\begin{theorem}结论.\end{theorem}'))
    def test_real_box(self): self.assertIn('decorative-box',errors(r'\begin{tcolorbox}x\end{tcolorbox}'))
    def test_verbatim_fake_box(self): self.assertFalse(errors(r'\begin{verbatim}\begin{tcolorbox}x\end{tcolorbox}\end{verbatim}'))
    def test_optional_title_not_silently_lost(self): self.assertIn('problem-title',errors(r'\begin{example}[题名]题面.\end{example}'))
    def test_side_effect_skipped(self): self.assertIn('skipped',instrument(doc(r'$x\label{a}$'))[1][0])
    def test_short_inline_retained(self): self.assertFalse(errors('设 $x>0$.'))

class ProjectTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); (self.root/'chapters').mkdir()
    def tearDown(self): self.tmp.cleanup()
    def write(self,p,s): q=self.root/p; q.parent.mkdir(parents=True,exist_ok=True); q.write_text(s,encoding='utf-8'); return q
    def test_nested_and_origins(self):
        p=self.write('main.tex',doc(r'\input{chapters/a}')); self.write('chapters/a.tex','A\n\\input{chapters/b}\n'); self.write('chapters/b.tex','B\n')
        x=expand_project(p); self.assertEqual(len(x.files),3); self.assertIn('B',x.text)
        line=x.text[:x.text.index('B\n',x.text.index('\\originalchapter'))].count('\n')+1
        self.assertEqual(x.location(line),('chapters/b.tex',1))
    def test_missing(self):
        p=self.write('main.tex',doc(r'\input{missing}'))
        with self.assertRaises(ProjectError): expand_project(p)
    def test_cycle(self):
        p=self.write('main.tex',doc(r'\input{chapters/a}')); self.write('chapters/a.tex',r'\input{main}')
        with self.assertRaises(ProjectError): expand_project(p)
    def test_outside(self):
        p=self.write('main.tex',doc(r'\input{../outside}'))
        with self.assertRaises(ProjectError): expand_project(p)
    def test_normalized_inside(self):
        p=self.write('main.tex',doc(r'\input{chapters/../inside}')); self.write('inside.tex','正文')
        self.assertEqual(len(expand_project(p).files),2)
    def test_comment_input_ignored(self): self.assertEqual(len(expand_project(self.write('main.tex',doc('% \\input{bad}\n正文'))).files),1)
    def test_bare_input(self):
        p=self.write('main.tex',doc('\\input chapters/a.tex\n')); self.write('chapters/a.tex','正文'); self.assertEqual(len(expand_project(p).files),2)
    def test_partial_unsupported_explicit(self):
        p=self.write('main.tex',doc(r'\includeonly{a}'))
        with self.assertRaises(ProjectError): expand_project(p)
    def test_symlink(self):
        p=self.write('main.tex',doc(r'\input{chapters/link}')); target=self.write('else.tex','x'); (self.root/'chapters/link.tex').symlink_to(target)
        with self.assertRaises(ProjectError): expand_project(p)
    def test_unrelated_bad_file_not_blocking(self):
        p=self.write('main.tex',doc('正文')); self.write('unused.tex',r'\write18{bad}'); self.assertFalse(any(x.severity in {'high','critical'} for x in scan_project(p)))
    def test_used_local_package_guarded(self):
        p=self.write('main.tex',doc(r'\usepackage{bad}')); self.write('bad.sty',r'\write18{bad}')
        self.assertTrue(any(x.severity=='critical' for x in scan_project(p)))
    def test_multiline_command_guarded(self): self.assertTrue(scan_text('\\write\n18{bad}','main.tex',self.root))
    def test_literal_guard_ignored(self): self.assertFalse(scan_text(r'\verb|\write18{bad}|','main.tex',self.root))
    def test_policy_bool_rejected(self):
        p=self.write('policy.json','{"inline_warning_ratio":true}')
        with self.assertRaises(ValueError): load_policy(p)
    def test_policy_unknown_rejected(self):
        p=self.write('policy.json','{"ignore_all_errors":true}')
        with self.assertRaises(ValueError): load_policy(p)
    def test_review_note_bound(self):
        p=self.write('main.tex','正文'); row={'level':'WARNING','file':'main.tex','line':1,'kind':'title-length-review'}
        pol=load_policy(None); pol['reviewed_warnings']=[dict(file='main.tex',line=1,kind='title-length-review',sha256=sha256(p),reason='确为标准专名')]
        self.assertFalse(annotate_warnings([row],pol,self.root)); self.assertTrue(row['reviewed'])
        p.write_text('新正文',encoding='utf-8'); self.assertTrue(annotate_warnings([dict(level='WARNING',file='main.tex',line=1,kind='title-length-review')],pol,self.root))
    def test_review_cannot_waive_error(self):
        p=self.write('main.tex','x'); row={'level':'ERROR','file':'main.tex','line':1,'kind':'empty-proof'}
        pol=load_policy(None); pol['reviewed_warnings']=[dict(file='main.tex',line=1,kind='empty-proof',sha256=sha256(p),reason='test')]
        annotate_warnings([row],pol,self.root); self.assertNotIn('reviewed',row)

class LogTests(unittest.TestCase):
    def test_tiny_overflow_review(self): r=audit(r'Overfull \hbox (0.2pt too wide)'); self.assertFalse(r['issues']); self.assertTrue(r['warnings'])
    def test_real_overflow_error(self): self.assertTrue(audit(r'Overfull \hbox (2.0pt too wide)')['issues'])
    def test_missing_glyph(self): self.assertTrue(audit('Missing character: no 字 in font')['issues'])
    def test_undefined_reference(self): self.assertTrue(audit("LaTeX Warning: Reference `x' undefined on page 1.")['issues'])
    def test_clean(self): self.assertFalse(audit('Output written on main.pdf')['issues'])

@unittest.skipUnless(os.environ.get('RUN_TEX_TESTS')=='1' and shutil.which('xelatex'),'Set RUN_TEX_TESTS=1 for real XeLaTeX tests')
class RealBuildTests(unittest.TestCase):
    def setUp(self): self.tmp=tempfile.TemporaryDirectory(prefix='数学 项目 '); self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def test_multifile_build_and_shared_records(self):
        (self.root/'chapters').mkdir(); main=self.root/'main.tex'
        main.write_text(doc('\\originalcontents\n\\input{chapters/a}\n\\include{chapters/b}'),encoding='utf-8')
        (self.root/'chapters/a.tex').write_text('\\originalsection{定义}\n设 $x>0$. 见式~\\eqref{eq:b}.\n',encoding='utf-8')
        (self.root/'chapters/b.tex').write_text('\\originalsection{结论}\n\\begin{equation}x=x.\\label{eq:b}\\end{equation}',encoding='utf-8')
        before=main.read_bytes(); r=build(main,self.root/'build'); self.assertGreaterEqual(r['record']['passes'],2); self.assertEqual(main.read_bytes(),before)
        self.assertEqual({x['path'] for x in r['record']['inputs']} & {'chapters/a.tex','chapters/b.tex'}, {'chapters/a.tex','chapters/b.tex'})
        from pdf_artifacts import render_pdf
        render_pdf(Path(r['pdf']),root=self.root)
        checks=verify_records(self.root,'build/main.build.json','build/main.render.json'); self.assertFalse(checks['errors'],checks)
    def test_measure_does_not_reject_wide_or_touch_source(self):
        main=self.root/'main with space.tex'; main.write_text(doc('$'+'+'.join('a_{'+str(i)+'}' for i in range(1,19))+'$'),encoding='utf-8')
        before=main.read_bytes(); r=measure(main); self.assertFalse(r['issues']); self.assertTrue(r['warnings']); self.assertEqual(main.read_bytes(),before); self.assertEqual(r['status'],'complete')
    def test_local_linewidth(self):
        main=self.root/'main.tex'; main.write_text(doc(r'\begin{minipage}{.25\linewidth}$a_1+a_2+a_3+a_4+a_5+a_6$\end{minipage}'),encoding='utf-8')
        r=measure(main); self.assertGreater(r['formulas'][0]['width_ratio'],.5)
    def test_failed_rebuild_cannot_reuse_old_evidence(self):
        main=self.root/'main.tex'; main.write_text(doc('正文 $x=1$.'),encoding='utf-8'); build(main,self.root/'build')
        main.write_text(doc(r'\UndefinedCommand'),encoding='utf-8')
        with self.assertRaises(RuntimeError): build(main,self.root/'build')
        data=json.loads((self.root/'build/main.build.json').read_text()); self.assertEqual(data['status'],'failed')
        self.assertTrue(verify_records(self.root,'build/main.build.json',None,False)['errors'])
    def test_missing_font_not_substituted(self):
        main=self.root/'main.tex'; main.write_text(doc('正文').replace('cmunrm.otf','NonexistentFont98765'),encoding='utf-8')
        with self.assertRaises(RuntimeError): build(main,self.root/'build')
        self.assertFalse((self.root/'build/main.pdf').exists())

if __name__=='__main__': unittest.main(verbosity=2)

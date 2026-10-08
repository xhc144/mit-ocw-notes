# MIT 18.335J Spring 2019 programming tasks, independently implemented.
# Reproduce with Julia 1.10 stdlibs only. No external packages or network used.
using LinearAlgebra, Random, Printf
Random.seed!(18335)
out=joinpath(@__DIR__,"julia-results")
mkpath(out)
report=String[]
check(name,b) = (b || error("failed: "*name); push!(report,name*": PASS"))
l4(x,y) = begin
    s=max(abs(x),abs(y))
    s==0 ? 0.0 : s*((abs(x)/s)^4+(abs(y)/s)^4)^(1/4)
end
cotdiff(x,y)=(sin(y)/sin(x))/sin(x+y)
check("PS1 Q1 exact integer boundary",Int64(Float64(Int64(2)^53+1)) != Int64(2)^53+1)
check("PS1 Q2 L4 underflow repaired",l4(1e-100,0.0)==1e-100)
check("PS1 Q2 L4 overflow repaired",l4(1e100,0.0)==1e100)
maxerr=0.0
setprecision(BigFloat,256) do
    for i in 1:10000
        x=(rand()-0.5)*10.0^rand(-300:300)
        y=(rand()-0.5)*10.0^rand(-300:300)
        s=max(abs(big(x)),abs(big(y)))
        ref=s==0 ? big(0) : s*((abs(big(x))/s)^4+(abs(big(y))/s)^4)^(big(1)/4)
        global maxerr=max(maxerr,Float64(abs(big(l4(x,y))-ref)/ref))
    end
end
check("PS1 Q2 L4 normal-range error < 20 eps",maxerr<20eps())
setprecision(BigFloat,1024) do
    ref=cot(big(1.0))-cot(big(1.0)+big(1e-20))
    check("PS1 Q2 cotdiff",Float64(abs(big(cotdiff(1.0,1e-20))-ref)/abs(ref))<5eps())
end
function newtonish(x)
    f=x^3-1; fp=3x^2; fpp=6x
    f==0 && return x
    D=fp^2-2f*fpp
    d=D<0 ? f/fp : 2f/(fp+copysign(sqrt(D),fp))
    x-d
end
setprecision(BigFloat,20000) do
    x=big(2); digits=Float64[]
    open(joinpath(out,"newton.csv"),"w") do io
        println(io,"step,digits,error_ratio_cubic")
        for k in 1:9
            prev=x-1; x=newtonish(x); err=x-1
            dig=-Float64(log10(abs(err)))
            push!(digits,dig)
            @printf(io,"%d,%.12f,%.12f\n",k,dig,Float64(err/prev^3))
        end
    end
    check("PS1 Q3 cubic convergence",abs(digits[7]/digits[6]-3)<0.01)
end
function pairwise(x,lo=firstindex(x),hi=lastindex(x),cutoff=1)
    n=hi-lo+1
    if n<=cutoff
        s=zero(eltype(x))
        for i in lo:hi
            s+=x[i]
        end
        return s
    end
    mid=(lo+hi)÷2
    pairwise(x,lo,mid,cutoff)+pairwise(x,mid+1,hi,cutoff)
end
open(joinpath(out,"summation.csv"),"w") do io
    println(io,"n,sequential,pairwise,blocked,bound_pairwise,bound_blocked")
    u=eps(Float32)/2
    for k in 4:18
        n=2^k; x=rand(Float32,n); ref=sum(Float64.(x)); scale=sum(abs,Float64.(x))
        seq=pairwise(x,1,n,n); pure=pairwise(x,1,n,1); block=pairwise(x,1,n,200)
        h=k; hb=199+max(0,ceil(Int,log2(n/200)))
        gp=h*u/(1-h*u);gb=hb*u/(1-hb*u)
        check("PS1 Q4 pairwise bound n=$n",abs(pure-ref)<=gp*scale)
        check("PS1 Q4 blocked bound n=$n",abs(block-ref)<=gb*scale)
        @printf(io,"%d,%.17g,%.17g,%.17g,%.17g,%.17g\n",n,abs(seq-ref)/ref,abs(pure-ref)/ref,abs(block-ref)/ref,gp*scale/ref,gb*scale/ref)
    end
end
A=randn(10,7); sub=A[[1,3,4],[2,3,5,6]]
check("PS2 Q2 submatrix induced norm",opnorm(sub)<=opnorm(A))
check("PS2 Q2 infinity norm source identity",opnorm(A,Inf)≈maximum(sum(abs,A,dims=2)))
X=rand(5,5);A=X'+X; T=copy(A);U=Matrix{Float64}(I,5,5)
steps=0
for k in 1:1000
    F=qr(T);Q=Matrix(F.Q);global T=F.R*Q; global U=U*Q
    global steps=k
    norm(T-Diagonal(diag(T)))<1e-12 && break
end
res=norm(A*U-U*Diagonal(diag(T)))/norm(A)
check("PS3 Q1 QR eigenvector residual",res<1e-10)
open(joinpath(out,"qr.txt"),"w") do io
    println(io,"steps=",steps,"\nrelative_eigen_residual=",res,"\neigenvalues=",diag(T))
end
open(joinpath(out,"checks.txt"),"w") do io
    println(io,"Julia ",VERSION,"; seed=18335; stdlibs LinearAlgebra, Random, Printf")
    println(io,"l4_max_relative_error=",maxerr)
    println(io,join(report,"\n"))
end
println("Julia assessment checks passed: ",length(report))

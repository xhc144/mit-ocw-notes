# Self-authored teaching experiments for real Float64 matrices.
# Checked against official Julia 1.x LinearAlgebra/SparseArrays API names.
# Not executed in the preparation environment (Julia is not installed).
using LinearAlgebra, SparseArrays, Random
Random.seed!(18335)

function gs_demo(A; modified=true)
    m, n = size(A)
    Q = zeros(Float64, m, n)
    R = zeros(Float64, n, n)
    for j in 1:n
        v = copy(A[:, j])
        for i in 1:j-1
            R[i, j] = dot(Q[:, i], modified ? v : A[:, j])
            v -= R[i, j] * Q[:, i]
        end
        R[j, j] = norm(v)
        R[j, j] > 0 || error("zero orthogonalization remainder")
        Q[:, j] = v / R[j, j]
    end
    return Q, R
end

function cg_demo(A, b; tol=1e-10, maxiter=length(b))
    x = zeros(Float64, length(b))
    r = b - A*x
    p = copy(r)
    rr = dot(r, r)
    scale = norm(b)
    history = [norm(r)]
    rr == 0 && return x, history
    for k in 1:maxiter
        q = A*p
        curvature = dot(p, q)
        curvature > 0 || error("A must be SPD in this demonstration")
        alpha = rr / curvature
        x += alpha*p
        r -= alpha*q
        rrnew = dot(r, r)
        true_residual = norm(b - A*x)
        push!(history, true_residual)
        if true_residual <= tol*scale
            return x, history
        end
        rrnew > 0 || error("recursive/true residual mismatch")
        p = r + (rrnew / rr)*p
        rr = rrnew
    end
    return x, history
end

# Experiment 1: near-dependent columns and orthogonality.
e = 1e-8
A = [1.0 1.0 1.0; e 0.0 0.0; 0.0 e 0.0; 0.0 0.0 e]
for modified in (false, true)
    Q, R = gs_demo(A; modified=modified)
    println((modified=modified, orth=opnorm(Q'*Q-I),
             factor=norm(A-Q*R)/norm(A)))
end
F = qr(A)
Q = Matrix(F.Q)[:, 1:size(A, 2)]
R = Matrix(F.R)
println((householder_orth=opnorm(Q'*Q-I),
         factor=norm(A-Q*R)/norm(A)))

# Experiment 2: residual is different from solution error.
A = Diagonal([1.0, 1e-12])
b = [1.0, 0.0]
xhat = [1.0, 1.0]
r = b-A*xhat
println((relative_residual=norm(r)/norm(b),
         relative_error=norm(xhat-[1.0, 0.0])))

# Experiment 3: power iteration and Rayleigh quotient.
A = Diagonal([4.0, 2.0, 1.0])
v = ones(3)/sqrt(3.0)
for k in 1:12
    v = A*v
    v /= norm(v)
    theta = dot(v, A*v)
    println((k=k, angle_sine=norm(v[2:3]),
             eigen_error=abs(theta-4.0), residual=norm(A*v-theta*v)))
end

# Experiment 4: one-dimensional Poisson, sparse Cholesky and CG.
n = 100
A = spdiagm(-1 => -ones(n-1), 0 => 2.0 .* ones(n), 1 => -ones(n-1))
xtrue = ones(n)
b = A*xtrue
F = cholesky(Symmetric(A))
xdirect = F \ b
xcg, history = cg_demo(A, b; tol=1e-10, maxiter=2*n)
println((nnz_A=nnz(A), nnz_L=nnz(sparse(F.L)),
         direct_residual=norm(b-A*xdirect),
         cg_residual=norm(b-A*xcg), steps=length(history)-1))

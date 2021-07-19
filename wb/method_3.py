# function rho=method_3(D,Aw,XYZw)
# % This function generates a reflectance vector for
# % method 3 (the object colors case), also called the
# % "LLSS" (Least Hyperbolic Tangent Slope Squared)
# % method. XYZw must fall within the object color solid.
# % The reflectance vector will have all elements within
# % the range 0-1.
#
# % D is nxn matrix of finite differencing constants.
# % Aw is nx3 matrix of illuminant-W-referenced CMFs.
# % XYZw is a three element vector of illum-W-referenced
# %      tristimulus values in the 0 <= Y <= 1  range.
# % rho is a nx1 vector of reflectance values (or zeros
# %      if failure).
#
# % Notes
# % -----
# % Version 2020_01_18 Scott Allen Burns
#
# % The input parameters d and cmfs_w can be generated by
# % method_3_prep. For a given illuminant, method_3_prep
# % needs to be called only once. Multiple calls to method_3
# % may then follow for various tristimulus values. This is a
# % typical use case, and avoids repeated computation of d and
# % cmfs_w.
# %
# % The XYZ_w supplied to method_3 must fall strictly within the
# % object color solid (i.e., be a valid object color that can be
# % represented by a reflectance curve strictly between 0 and 1),
# % or the method will fail and return a vector of zeros.
# %
# % The reflectance curve generated will always have values in
# % the range 0 to 1, corresponding to valid object colors. If
# % it is desired to expand the applicability of the method to
# % any real color within the spectral locus (including emissive
# % colors), use method_2 instead.
# %
# % method_3 is based on "method 3" of Reference [1]. It also
# % corresponds to method "LHTSS" (Least Hyperbolic Tangent Slope
# % Squared) of Reference [2].
# %
# % References
# % ----------
# % [1] Burns SA. Numerical methods for smoothest reflectance
# %     reconstruction. Color Research & Application, Vol 45,
# %     No 1, 2020, pp 8-21.
# % [2] Generating Reflectance Curves from sRGB Triplets, 2015
# %     http://scottburns.us/reflectance-curves-from-srgb/#LHTSS

n=size(Aw,1)
rho=zeros(n,1); z=zeros(n,1); lambda=zeros(3,1)
count=0; % iteration counter
maxit=20; % max number of iterations
ftol=1.0e-8; % convergence tolerance
warning('off','all');
while count <= maxit
    r=(tanh(z)+1)/2; d1=diag((sech(z).^2)/2); d1a=d1*Aw;
    d2=diag(sech(z).^2.*tanh(z));
    F=[D*z+d1a*lambda; Aw'*r-XYZw(:)];
    J=[D-diag(d2*Aw*lambda), d1a; d1a', zeros(3)];
    try
        delta=J\(-F); % solve system of equations J*delta = -F
    catch
        disp('Ill-conditioned or singular linear system detected.');
        disp('Check to make sure XYZw is within the object color solid.');
        warning('on','all')
        return
    end
    z=z+delta(1:n);
    lambda=lambda+delta(n+1:n+3);
    if all(abs(F)<ftol) % convergence check
        rho=(tanh(z)+1)/2;
        warning('on','all');
        return
    end
    count=count+1;
end
disp('Maximum number of iterations reached.');
disp('Check to make sure XYZw is within the object color solid.');
warning('on','all')
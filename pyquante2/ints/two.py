"""
 Copyright (c) 2004, Richard P. Muller. All Rights Reserved. 

 PyQuante version 2.0 and later is covered by the GPL
 license. Please see the file LICENSE that is part of this
 distribution. 

"""

from numpy import array,pi,sqrt,exp
from math import factorial
from pyquante2.utils import Fgamma, norm2, isnear
from pyquante2.ints.one import gaussian_product_center, binomial_prefactor


def ERI(a,b,c,d):
    """
    >>> from pyquante2.utils import isnear
    >>> from pyquante2.basis.pgbf import pgbf
    >>> s = pgbf(1)
    >>> isnear(ERI(s,s,s,s),1.1283791671)
    True
    >>> from pyquante2.basis.cgbf import cgbf
    >>> s = cgbf(exps=[1],coefs=[1])
    >>> isnear(ERI(s,s,s,s),1.1283791671)
    True
    >>> s2 = cgbf((0,0,1),(0,0,0),[1],[1])
    >>> isnear(ERI(s,s,s2,s2),0.84270079)
    True
    """ 
    if d.contracted:
        return sum(cd*ERI(pd,c,a,b) for (cd,pd) in d)
    return coulomb_repulsion(a.origin,a.norm,a.powers,a.exponent,
                             b.origin,b.norm,b.powers,b.exponent,
                             c.origin,c.norm,c.powers,c.exponent,
                             d.origin,d.norm,d.powers,d.exponent)

def coulomb_repulsion(xyza,norma,(la,ma,na),alphaa,
                      xyzb,normb,(lb,mb,nb),alphab,
                      xyzc,normc,(lc,mc,nc),alphac,
                      xyzd,normd,(ld,md,nd),alphad):
    """
    Return the coulomb repulsion between four primitive gaussians a,b,c,d with the given origin
    x,y,z, normalization constants norm, angular momena l,m,n, and exponent alpha.
    >>> p1 = array((0.,0.,0.),'d')
    >>> p2 = array((0.,0.,1.),'d')
    >>> lmn = (0,0,0)
    >>> isnear(coulomb_repulsion(p1,1.,lmn,1.,p1,1.,lmn,1.,p1,1.,lmn,1.,p1,1.,lmn,1.),4.3733545819)
    True
    >>> isnear(coulomb_repulsion(p1,1.,lmn,1.,p1,1.,lmn,1.,p2,1.,lmn,1.,p2,1.,lmn,1.),3.2661267318)
    True
    """
    xa,ya,za = xyza
    xb,yb,zb = xyzb
    xc,yc,zc = xyzc
    xd,yd,zd = xyzd

    rab2 = norm2(xyza-xyzb)
    rcd2 = norm2(xyzc-xyzd)
    xyzp = gaussian_product_center(alphaa,xyza,alphab,xyzb)
    xp,yp,zp = xyzp
    xyzq = gaussian_product_center(alphac,xyzc,alphad,xyzd)
    xq,yq,zq = xyzq
    rpq2 = norm2(xyzp-xyzq)
    gamma1 = alphaa+alphab
    gamma2 = alphac+alphad
    delta = 0.25*(1/gamma1+1/gamma2)

    Bx = B_array(la,lb,lc,ld,xp,xa,xb,xq,xc,xd,gamma1,gamma2,delta)
    By = B_array(ma,mb,mc,md,yp,ya,yb,yq,yc,yd,gamma1,gamma2,delta)
    Bz = B_array(na,nb,nc,nd,zp,za,zb,zq,zc,zd,gamma1,gamma2,delta)

    sum = 0.
    for I in xrange(la+lb+lc+ld+1):
        for J in xrange(ma+mb+mc+md+1):
            for K in xrange(na+nb+nc+nd+1):
                sum = sum + Bx[I]*By[J]*Bz[K]*Fgamma(I+J+K,0.25*rpq2/delta)

    return 2*pow(pi,2.5)/(gamma1*gamma2*sqrt(gamma1+gamma2)) \
           *exp(-alphaa*alphab*rab2/gamma1) \
           *exp(-alphac*alphad*rcd2/gamma2)*sum*norma*normb*normc*normd

def B_term(i1,i2,r1,r2,u,l1,l2,l3,l4,Px,Ax,Bx,Qx,Cx,Dx,gamma1,gamma2,delta):
    "THO eq. 2.22"
    return fB(i1,l1,l2,Px,Ax,Bx,r1,gamma1) \
           *pow(-1,i2)*fB(i2,l3,l4,Qx,Cx,Dx,r2,gamma2) \
           *pow(-1,u)*fact_ratio2(i1+i2-2*(r1+r2),u) \
           *pow(Qx-Px,i1+i2-2*(r1+r2)-2*u) \
           /pow(delta,i1+i2-2*(r1+r2)-u)

def B_array(l1,l2,l3,l4,p,a,b,q,c,d,g1,g2,delta):
    Imax = l1+l2+l3+l4+1
    B = [0]*Imax
    for i1 in xrange(l1+l2+1):
        for i2 in xrange(l3+l4+1):
            for r1 in xrange(i1/2+1):
                for r2 in xrange(i2/2+1):
                    for u in xrange((i1+i2)/2-r1-r2+1):
                        I = i1+i2-2*(r1+r2)-u
                        B[I] = B[I] + B_term(i1,i2,r1,r2,u,l1,l2,l3,l4,
                                             p,a,b,q,c,d,g1,g2,delta)
    return B

def fB(i,l1,l2,P,A,B,r,g): return binomial_prefactor(i,l1,l2,P-A,P-B)*B0(i,r,g)
def B0(i,r,g): return fact_ratio2(i,r)*pow(4*g,r-i)
def fact_ratio2(a,b): return factorial(a)/factorial(b)/factorial(a-2*b)

if __name__ == '__main__':
    import doctest; doctest.testmod()

! qinit routine for parabolic bowl problem, only single layer
subroutine qinit(meqn,mbc,mx,my,xlower,ylower,dx,dy,q,maux,aux)

    use geoclaw_module, only: grav

    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn,mbc,mx,my,maux
    real(kind=8), intent(in) :: xlower,ylower,dx,dy
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)

    ! Parameters for problem
    real(kind=8) D0, L, eta0

    ! Other storage
    integer :: i,j
    real(kind=8) :: omega,x,y,eta,t0,A,denom

    common /cparam/ D0, L, eta0
    
    omega = sqrt(8.*grav*D0 / L**2)
    t0 = 0.  ! if not, would have to set u,v different from 0
    A = ((D0 + eta0)**2 - D0**2) / ((D0 + eta0)**2 + D0**2)
    denom = 1 - A*cos(omega*t0)
    
    do i=1-mbc,mx+mbc
        x = xlower + (i - 0.5d0)*dx
        do j=1-mbc,my+mbc
            y = ylower + (j - 0.5d0) * dy
            eta = D0 * (sqrt(1-A**2)/denom - 1 \
                  - (x**2 + y**2)/L**2 * ((1-A**2)/(1-A*cos(omega*t0))**2 - 1))
            
            q(1,i,j) = max(0.d0,eta - aux(1,i,j))
            q(2,i,j) = 0.d0
            q(3,i,j) = 0.d0
        enddo
    enddo
    
end subroutine qinit

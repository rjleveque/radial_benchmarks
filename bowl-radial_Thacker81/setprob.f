c     ==================
      subroutine setprob
c     ==================

      implicit none
      real(kind=8) :: D0,L,eta0
      character*12 :: fname
      integer :: iunit
      common /cparam/ D0, L, eta0
c
c
      iunit = 7
      fname = 'setprob.data'
c     # open the unit with new routine from Clawpack 4.4 to skip over
c     # comment lines starting with #:
      call opendatafile(iunit, fname)
                

c
      read(7,*) D0
      read(7,*) L
      read(7,*) eta0

      return
      end

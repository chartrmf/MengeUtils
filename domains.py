# Classes for specifying domains

from primitives import Vector2
import copy
import numpy as np

class RectDomain:
    '''A simple class to represent a rectangular domain'''
    def __init__( self, minCorner, size ):
        '''RectDomain constructor.
        @param  minCorner       A 2-tuple-like instace of floats.  The position, in world space,
                                of the "bottom-left" corner of the domain.  (Minimum x- and y-
                                values.
        @param  size            A 2-tuple-like instace of floats.  The span of the domain (in world
                                space.)  The maximum values of the domain are minCorner[0] + size[0]
                                and minCorner[1] + size[1], respectively.
        '''
        self.minCorner = minCorner
        self.size = size

    def __str__( self ):
        return 'RectDomain from ( %.2f, %.2f ) to ( %.2f, %.2f )' % ( self.minCorner[0], self.minCorner[1],
                                                                      self.minCorner[0] + self.size[0], self.minCorner[1] + self.size[1] )

    def __eq__( self, other ):
        '''Reports if the two domains are equivalent.

        Equivalency implied by covering the same domain.minCorner

        @param  other       An instance of RectDomain.copyDomain
        @returns        A boolean.  True if they are equivalent, false otherwise.
        '''
        return self.minCorner == other.minCorner and self.size == other.size
        
    def intersects( self, domain ):
        '''Reports if this domain intersects the given domain.minCorner

        @param      domain      An instance of RectDomain.
        @returns    A boolean.  True if the two domains intersect, False
                    otherwise.
        '''
        return not ( self.minCorner[0] > domain.minCorner[0] + domain.size[0] or
                     self.minCorner[1] > domain.minCorner[1] + domain.size[1] or
                     self.minCorner[0] + self.size[0] < domain.minCorner[0] or
                     self.minCorner[1] + self.size[1] < domain.minCorner[1] )

    def copyDomain( self, domain ):
        '''Copies the domain settings from the given domain to this domain'''
        self.minCorner = copy.deepcopy( domain.minCorner )
        self.size = copy.deepcopy( domain.size )

    def pointInside( self, point ):
        '''Reports if the given point is inside the domain.minCorner

        @param      point       A 2-tuple like class with floats.  The x- and y-values
                                of the point in world space.
        @returns    A boolean.  True if the point lies inside (including on the boundary)
                    False, otherwise.
        '''
        localX = point[0] - self.minCorner[0]
        localY = point[1] - self.minCorner[1]
        return ( localX >= 0 and localY >= 0 and
                 localX <= self.size[0] and localY <= self.size[1] )

    def reflectPoint( self, point ):
        '''Given a point INSIDE the domain, returns four points.  The reflection of the point over
            all domain boundaries.

            It is the caller's responsibility to only call this function on a point that is KNOWN
            to be inside the domain.  Otherwise, the reflection values will not be meaningful.

        @param      point       A 2-tuple like class with floats.  The x-and y-values of the point
                                in world space.
        @returns    A 4 x 2 numpy array.  Each row is a reflected point: left, right, bottom, top.
        '''
        reflection = np.empty( ( 4, 2 ), dtype=np.float32 )
        l = self.minCorner[0]
        b = self.minCorner[1]
        r = l + self.size[0]
        t = b + self.size[1]

        # left
        reflection[ 0, : ] = ( 2 * l - point[0], point[1] )
        # right
        reflection[ 1, : ] = ( 2 * r - point[0], point[1] )
        # bottom
        reflection[ 2, : ] = ( point[0], 2 * b - point[1] )
        # top
        reflection[ 3, : ] = ( point[0], 2 * t - point[1] )
        
        return reflection

    def intersection( self, domain ):
        '''Computes the intersection of two domains and reports it as a domain.minCorner

        @param      domain      An instance of RectDomain.  The domain to intersect.
        @returns    A RectDomain instance covering the region of intersection.  Returns None if
                    there is no intersection.
        '''
        if ( not self.intersects( domain ) ):
            return None
        # there is an intersection
        X = [ self.minCorner[0], domain.minCorner[0],
              self.minCorner[0] + self.size[0], domain.minCorner[0] + domain.size[0] ]
        X.sort()
        Y = [ self.minCorner[1], domain.minCorner[1],
              self.minCorner[1] + self.size[1], domain.minCorner[1] + domain.size[1] ]
        Y.sort()
        minCorner = Vector2( X[1], Y[1] )
        maxCorner = Vector2( X[2], Y[2] )
        return RectDomain( minCorner, maxCorner - minCorner )        
    

if __name__ == '__main__':
    def testIntersection():
        print "Testing rect domain intersection"
        d = RectDomain( Vector2( 0, 0 ), Vector2( 5, 5 ) )
        # test cases consist of pairs: an domain to intersect with d, and the expected result.
        testCases = [ ( RectDomain( Vector2( 6, 6 ),   Vector2( 1, 1 ) ),   None ),
                      ( RectDomain( Vector2( 1, 1 ),   Vector2( 3, 3 ) ),   RectDomain( Vector2( 1, 1 ), Vector2( 3, 3 ) ) ),
                      ( RectDomain( Vector2( -1, -1 ), Vector2( 2, 2 ) ),   RectDomain( Vector2( 0, 0 ), Vector2( 1, 1 ) ) ),
                      ( RectDomain( Vector2( -1, 1 ),  Vector2( 2, 2 ) ),   RectDomain( Vector2( 0, 1 ), Vector2( 1, 2 ) ) ),
                      ( RectDomain( Vector2( -1, 1 ),  Vector2( 2, 2 ) ),   RectDomain( Vector2( 0, 1 ), Vector2( 1, 2 ) ) ),
                      ]
        for dTest, expInter in testCases:
            result = d.intersection( dTest )
            if ( result == expInter ):
                print "\tPASS!"
            else:
                print "\tFAIL!"
                print "\t\t%s n %s" % ( d, dTest )
                print "\t\tEXPECTED:\n\t\t", expInter
                print "\t\tGOT:    \n\t\t", result
                

    testIntersection()     
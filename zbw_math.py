import maya.cmds as cmds
import math

def vectorLength(vec=(0,0,0),*args):
    """
    finds the length of the vector
    """
    A0 = vec[0]
    A1 = vec[1]
    A2 = vec[2]

    length = math.sqrt(A0**2 + A1**2 + A2**2)

    return length

def normalizeVector(vec=(0,0,0), *args):
    """
    normalizes the vector so all three axes are from 0-1
    """
    A0 = vec[0]
    A1 = vec[1]
    A2 = vec[2]

    length = vectorLength(vec)
    normalVec = [A0/length, A1/length, A2/length]

    return normalVec

def dotProduct(vecA = [1,2,3], vecB = [4,5,6], *args):
    """
    returns the dot product of two vecs. This is the projection of one vector onto another (first onto second)
    """
    A0 = vecA[0]
    A1 = vecA[1]
    A2 = vecA[2]

    B0 = vecB[0]
    B1 = vecB[1]
    B2 = vecB[2]

    dot = A0*B0 + A1*B1 + A2*B2

    return dot

def dotNormalized(vecA = [1,2,3], vecB = [4,5,6], *args):
    """
    returns the normalized dot product (projection of first onto second from 0-1)
    """
    normA = normalizeVector(vecA)
    normB = normalizeVector(vecB)

    dotNorm = dotProduct(normA, normB)

    return dotNorm

def angleBetween(vecA, vecB, *args):
    """
    finds the angle between two vectors (in degrees)
    """
    dot = dotNormalized(vecA, vecB)

    rads = math.acos(dot)
    degrees = rads*(180/math.pi)

    return degrees



screenWidth = 640
screenHeight = 480

def findMid(p1, p2):
    endpoint = []
    for xy in range(2):
        endpoint.append(abs(p1[xy] + (p2[xy] - p1[xy]) / 2))
    return tuple(endpoint)

def createLightning(startPoint,endPoint,maxDepth):
    points = [startPoint,endPoint]
    for times in range(maxDepth):

    return points

if __name__ == "__main__":
    startPoint = (0,screenHeight/2)
    endPoint = (screenWidth, screenHeight/2)
    print(findMid(startPoint, endPoint))

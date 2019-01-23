import pygame
from enums import DebugShape

class DebugDrawing():
    def draw(list, screen):
        dirtyRects = []
        for obj in list:
            if 'shape' in obj:
                shape = obj['shape']
                if shape == DebugShape.LINE:
                    r = pygame.draw.line(screen, obj['c'], obj['sp'], obj['ep'], obj['w'])
                    dirtyRects.append(r)
                elif shape == DebugShape.RECT:
                    r = pygame.draw.rect(screen, obj['c'], obj['r'], obj['w'])
                    dirtyRects.append(r)
                elif shape == DebugShape.ELLIPSE:
                    r = pygame.draw.ellipse(screen, obj['c'], obj['r'], obj['w'])
                    dirtyRects.append(r)
                elif shape == DebugShape.POLYGON:
                    r = pygame.draw.polygon(screen, obj['c'], obj['v'], obj['w'])
                    dirtyRects.append(r)
        return dirtyRects

    def line(color, startPos, endPos, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.LINE
        obj['sp'] = startPos
        obj['ep'] = endPos
        obj['w'] = width
        return obj

    def ellipse(color, rect, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.ELLIPSE
        obj['r'] = rect
        obj['w'] = width
        return obj

    def rect(color, rect, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.RECT
        obj['r'] = rect
        obj['w'] = width
        return obj

    def polygon(color, vertices, width = 1):
        obj = {}
        obj['c'] = color
        obj['shape'] = DebugShape.POLYGON
        obj['v'] = vertices
        obj['w'] = width
        return obj
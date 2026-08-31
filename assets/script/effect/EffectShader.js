/**
 * Shader
 */

var shaderPrograms = {}

setShader = (node, shaderName) => {
    
}

setGray = (sprite, gray) => {
    if (gray) {
        sprite.setState(1)
    } else {
        sprite.setState(0)
    }
}

setShadow = (node, opacity, disable) => {
    if (typeof opacity == "boolean") {
        disable = opacity
        opacity = 50
    } else {
        opacity = opacity || 50
    }

    if (disable) {
        node.color = COLOR.WHITE
        node.opacity = node.__oriOpacity__ || 255
    } else {
        node.color = COLOR.BLACK
        node.__oriOpacity__ = node.opacity
        node.opacity = opacity
    }
}

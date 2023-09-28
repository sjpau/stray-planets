#version 330 core

in vec2 vert;
in vec2 textcoord;

out vec2 uvs;

void main() {
    uvs = textcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
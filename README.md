# 🖥️ CSE423 — Computer Graphics

**BRAC University | Department of Computer Science and Engineering**

A collection of OpenGL programs, lab assignments, and mini-games built throughout the CSE423 Computer Graphics course. Everything is written in **Python with PyOpenGL** using the fixed-function pipeline — no game engine, no shortcuts, just raw OpenGL, GLUT, and math.

> This repo also served as the foundation for the course project → [⛩️ Aegis: Domain of Echoes](https://github.com/Hibrul-Anam-Prantik/Aegis-Domain-of-Echoes)

---

## 📁 Contents

### 🎮 Mini-Games

#### 🔫 BulletFrenzy

A **3D top-down arena shooter** built with PyOpenGL.

- Survive waves of pulsing red enemies in a colored checkerboard arena
- Move with `W/S`, rotate your gun with `A/D`, and shoot with **Left Click**
- Enemies pursue the player using vector-based AI and respawn on hit
- Lose condition: miss 10 bullets or let enemies reach you 5 times
- Features **first-person mode** (Right Click toggle), **cheat mode** (`C`) with auto-aim, and **cheat vision** (`V`)
- Camera orbits with Arrow Keys; zoom with Up/Down

**Key concepts:** 3D camera (`gluLookAt`), enemy AI, bullet physics, collision detection, HUD rendering

---

#### 💎 CatchTheDiamonds

A **2D arcade catch game** built from scratch using the **Midpoint Line Algorithm** — no `glLine`, every line drawn pixel by pixel.

- Move your catcher with Arrow Keys to catch falling diamonds
- Each catch increases speed and randomizes the diamond's color
- Miss one diamond and it's game over
- Features **cheat mode** (`C`) where the catcher auto-chases the diamond
- UI buttons drawn with the line algorithm: Restart, Pause/Resume, Exit

**Key concepts:** Midpoint line algorithm, zone-based octant mapping, 2D collision detection, game state management

---

#### 🏠 House_in_Rainfall

An **animated 2D scene** of a house in rainfall, rendered with OpenGL primitives.

**Key concepts:** Scene composition, animation, `GL_POINTS` for particles

---

#### 📦 AmazingBox

An OpenGL program exploring **3D box/cube** rendering and transformations.

**Key concepts:** `glutSolidCube`, matrix transformations, 3D rendering basics

---

### 📂 Lab Assignments

#### Lab01

Introductory OpenGL exercises — window setup, basic shapes, color, and the rendering pipeline.

#### Lab03

Intermediate exercises — transformations, camera setup, and 3D primitives.

---

## 🛠️ Setup & Running

**Install dependencies:**

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

**Run any program:**

```bash
python BulletFrenzy.py
python CatchTheDiamonds.py
python House_in_Rainfall.py
python AmazingBox.py
```

---

## 🕹️ Controls Summary

| Game             | Move             | Action             | Special                                      |
| ---------------- | ---------------- | ------------------ | -------------------------------------------- |
| BulletFrenzy     | `W/S`            | Left Click — shoot | `C` cheat, `V` vision, Right Click — FP mode |
| CatchTheDiamonds | `←/→` Arrow Keys | Mouse — UI buttons | `C` cheat mode                               |

---

## 🔗 Related

- **Course Project:** [⛩️ Aegis: Domain of Echoes](https://github.com/Hibrul-Anam-Prantik/Aegis-Domain-of-Echoes) — a full 3D arena-defense game built as the CSE423 final project

---

## 👤 Author

**Hibrul Anam Prantik** — [@Hibrul-Anam-Prantik](https://github.com/Hibrul-Anam-Prantik)
BRAC University, CS Undergrad

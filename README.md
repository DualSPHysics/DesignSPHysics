# DesignSPHysics

**DesignSPHysics** is an open-source FreeCAD module that provides a comprehensive graphical user interface (GUI) for [DualSPHysics](http://dual.sphysics.org/), a mesh-free particle-based fluid simulation engine based on Smoothed Particle Hydrodynamics (SPH). 

Development of DesignSPHysics began in September 2016, and the software is currently in its beta phase.

Visit the [official DesignSPHysics website](http://design.sphysics.org) for downloads, tutorials, and additional information.

![Screenshot](https://design.sphysics.org/img/github-shot-21112019.png)

---

## 📢 News

### Upcoming Events
- **[19th SPHERIC World Conference](https://spheric2025.upc.edu/)** — Barcelona, Spain — *June 16–19, 2025*
- **[8th DualSPHysics Workshop](https://dual.sphysics.org/8thworkshop/)** — Ourense, Spain — *January 27–29, 2026*

### Recent Past Events
- **[SPH Modelling for Engineering Applications](https://sites.google.com/view/hykudsph/home?authuser=0)** — Braunschweig, Germany — *March 25–27, 2025*
- **[4th Hands-on Course on Experimental and Numerical Modelling of Wave-Structure Interaction](https://sites.google.com/unifi.it/hands-on-course-2024)** — Florence, Italy — *July 1–5, 2024*
- **[7th DualSPHysics Workshop](https://dual.sphysics.org/7thworkshop/)** — Bari, Italy — *March 19–21, 2024*


> Visit the [official DesignSPHysics website](https://dual.sphysics.org/training/) for more information.

---

## 🚀 Latest Releases

- [v0.8.1](https://github.com/DualSPHysics/DesignSPHysics/releases/tag/0.8.1) — *May 27, 2025* ([Changelog](CHANGELOG.md))
- [v0.7.0](https://github.com/DualSPHysics/DesignSPHysics/releases/tag/0.7.0) — *September 15, 2023*

---

## 🧩 Features

DesignSPHysics simplifies the process of setting up, running, and post-processing SPH simulations through an intuitive interface in FreeCAD. Key functionalities include:

- Integrated pre-processing with **GenCase**
- Simulation execution with **DualSPHysics**
- Post-processing using **DualSPHysics Tools**
- Case creation with fluid and solid domains
- Automated data generation and file management
- Built-in support for Python 3.5+ and Qt via PySide
- Macro bootstrapper integration with FreeCAD

Future versions will include modular support for additional SPH solvers beyond DualSPHysics.

---

## ⚙️ Setup

There are multiple ways to obtain the DesignSPHysics package:

### 📥 Option 1: Clone the Repository

Clone the latest development version from GitHub:
```bash
git clone https://github.com/DualSPHysics/DesignSPHysics.git
```

### 📦 Option 2: Download a Stable Release

Get pre-packaged code from the [GitHub Releases page](https://github.com/DualSPHysics/DesignSPHysics/releases).

---

### 🔧 DualSPHysics Binaries

> **Important:** Starting with version 0.8.0, DesignSPHysics does **not** include the DualSPHysics binaries. These must be downloaded separately.

DualSPHysics binaries should be located in `DesignSPHysics/dualsphysics/bin`. 
You can obtain the required binaries using one of the following methods:

- **Option A: Automatically via Setup Script**
  ```bash
  cd DesignSPHysics
  chmod +x setup.sh && ./setup.sh
  ```

- **Option B: Manually**
  1. Download `dualsphysics.zip` from the [official DualSPHysics website](https://dual.sphysics.org/sphcourse/DualSPHysics-bin)
  2. Move the file into the `DesignSPHysics` folder
  3. Extract the contents

---

## 🛠 Installation Instructions

### Installing a Development Build

1. Rename the downloaded or cloned folder to `DesignSPHysics`
2. Move the folder into FreeCAD’s `Mod` directory:
   - **Windows:** `%APPDATA%/FreeCAD/Mod`
   - **Linux:** `~/.FreeCAD/Mod`
3. Copy the `DesignSPHysics.FCMacro` file into the FreeCAD `Macro` directory:
   - **Windows:** `%APPDATA%/FreeCAD/Macro`
   - **Linux:** `~/.FreeCAD/Macro`

---

## ▶️ Launching DesignSPHysics

To start using the plugin in FreeCAD:

1. Open **FreeCAD**
2. Navigate to **Macro → Macros...**
3. In the `Execute macro` window:
   - Locate and select `DesignSPHysics.FCMacro`
   - Click **Execute**

A new panel labeled **DesignSPHysics** will appear on the right. Follow these steps:

4. Click **Setup Plugin** to open the **DSPH Setup** window
5. DualSPHysics executables should be configured automatically while ParaView executable should be configured manually.

---

## 🛠️ Troubleshooting

If you experience issues during installation or launch, residual configuration files from previous installations might be the cause. You should delete them before proceeding.

### Configuration File Locations

- **Windows:**
  ```
  C:\Users\<user>\AppData\Roaming\FreeCAD
  ```

- **Linux:**
  ```
  ~/.config/FreeCAD
  ```

To manually remove residual files:
- Use a file manager to delete any `DesignSPHysics`-related files
- Or, run this command in a terminal (Linux):
  ```bash
  rm ~/.config/FreeCAD/designsphysics*
  ```

> Replace `<user>` with your actual system username.


---

## 📚 Documentation & Support

- 📖 [DesignSPHysics Wiki](https://github.com/DualSPHysics/DesignSPHysics/wiki)
- 💬 [DualSPHysics GitHub Discussions](https://github.com/DualSPHysics/DualSPHysics/discussions)
- 🐛 [Report Issues on GitHub](https://github.com/DualSPHysics/DesignSPHysics/issues)
- ✉️ Contact contributors via the [CONTRIBUTING file](CONTRIBUTING.md)

---

## 🤝 Contributing

We welcome contributions! Whether it’s bug fixes, new features, or documentation improvements, your input is valuable. Please read the [CONTRIBUTING file](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

**DesignSPHysics** is released under the [GNU General Public License v3.0 or later](http://www.gnu.org/licenses/).

```
© 2025 Ivan Martinez Estevez, Andres Vieira

EPHYSLAB Environmental Physics Laboratory, Universidade de Vigo  
EPHYTECH Environmental Physics Technologies
```

> This software is provided “as is,” without warranty of any kind. See the license for details.

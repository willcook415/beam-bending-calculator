import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

st.set_page_config(page_title="Beam Bending Calculator", layout="centered")
st.title("🧮 Beam Bending Calculator")
st.markdown("Calculate diagrams for a simply supported beam with point loads, UDLs, and applied moments.")

# Beam and material properties
L = st.number_input("Beam Length (m)", min_value=1.0, max_value=100.0, value=10.0)
E = st.number_input("Young's Modulus (GPa)", min_value=1.0, max_value=500.0, value=200.0)
I = st.number_input("Moment of Inertia (cm⁴)", min_value=1.0, max_value=1e5, value=5000.0)
E *= 1e9
I *= 1e-8

# Point loads
num_loads = st.slider("Number of Point Loads", 0, 5, value=2)
loads = []
st.subheader("📌 Point Load Inputs")
for i in range(num_loads):
    mag = st.number_input(f"Load {i+1} Magnitude (kN)", value=10.0, key=f"mag_{i}")
    pos = st.number_input(f"Load {i+1} Position (m)", value=2.0 + i, key=f"pos_{i}")
    if pos > L:
        st.error(f"Load {i+1} position must be within the beam.")
        st.stop()
    loads.append((mag * 1e3, pos))

# UDL
st.subheader("🌧️ UDL Input")
use_udl = st.checkbox("Include a UDL?")
w = a_udl = b_udl = 0
if use_udl:
    w = st.number_input("UDL Magnitude (kN/m)", value=2.0) * 1e3
    a_udl = st.number_input("UDL Start (m)", value=2.0)
    b_udl = st.number_input("UDL End (m)", value=6.0)
    if a_udl > b_udl or b_udl > L:
        st.error("Invalid UDL range.")
        st.stop()

# Moment loads
num_moments = st.slider("Number of Applied Moments", 0, 3, value=1)
moments = []
st.subheader("🔁 Moment Load Inputs")
for i in range(num_moments):
    mag = st.number_input(f"Moment {i+1} Magnitude (kNm)", value=5.0, key=f"mmag_{i}") * 1e3
    pos = st.number_input(f"Moment {i+1} Position (m)", value=4.0 + i, key=f"mpos_{i}")
    if pos > L:
        st.error(f"Moment {i+1} position must be within the beam.")
        st.stop()
    moments.append((mag, pos))

# Reaction calculations
total_point_load = sum([mag for mag, _ in loads])
udl_load = w * (b_udl - a_udl) if use_udl else 0
udl_centroid = (a_udl + b_udl) / 2 if use_udl else 0
moment_about_A = sum([mag * pos for mag, pos in loads]) + udl_load * udl_centroid + sum([-M for M, pos in moments])
total_load = total_point_load + udl_load
RB = moment_about_A / L
RA = total_load - RB

st.subheader("🔧 Reaction Forces")
st.write(f"Left Support (RA): {RA/1e3:.2f} kN")
st.write(f"Right Support (RB): {RB/1e3:.2f} kN")

x_vals = np.linspace(0, L, 1000)
dx = x_vals[1] - x_vals[0]
V = np.full_like(x_vals, RA)
M = RA * x_vals

for mag, pos in loads:
    V -= mag * (x_vals >= pos)
    M -= mag * np.where(x_vals >= pos, x_vals - pos, 0)

if use_udl:
    udl_zone = (x_vals >= a_udl) & (x_vals <= b_udl)
    x_udl = x_vals[udl_zone]
    V[udl_zone] -= w * (x_udl - a_udl)
    V[x_vals > b_udl] -= w * (b_udl - a_udl)
    M[udl_zone] -= w * (x_udl - a_udl)**2 / 2
    M[x_vals > b_udl] -= w * ((b_udl - a_udl)**2 / 2 + (x_vals[x_vals > b_udl] - b_udl) * (b_udl - a_udl))

for mag, pos in moments:
    M += mag * (x_vals >= pos)

theta = np.cumsum(M / (E * I)) * dx
y = np.cumsum(theta) * dx
y -= y.min()

fig, axs = plt.subplots(5, 1, figsize=(10, 14))
fig.tight_layout(pad=4)

axs[0].plot(x_vals, V / 1e3, color='blue')
axs[0].set_title("Shear Force Diagram")
axs[0].set_ylabel("Shear (kN)")
axs[0].grid(True)

axs[1].plot(x_vals, M / 1e3, color='red')
axs[1].set_title("Bending Moment Diagram")
axs[1].set_ylabel("Moment (kNm)")
axs[1].grid(True)

axs[2].plot(x_vals, theta, color='purple')
axs[2].set_title("Slope")
axs[2].set_ylabel("Slope (rad)")
axs[2].grid(True)

axs[3].plot(x_vals, y * 1e3, color='green')
axs[3].set_title("Deflection")
axs[3].set_ylabel("Deflection (mm)")
axs[3].grid(True)

axs[4].plot([0, L], [0, 0], 'k-', linewidth=3)
axs[4].set_title("Beam Diagram")
axs[4].set_ylim(-1, 2)
axs[4].axis('off')
axs[4].text(0, -0.4, "RA", ha='center', fontsize=10)
axs[4].text(L, -0.4, "RB", ha='center', fontsize=10)
for i, (mag, pos) in enumerate(loads):
    axs[4].arrow(pos, 1.5, 0, -1, head_width=0.1, head_length=0.2, fc='blue', ec='blue')
    axs[4].text(pos, 1.6, f"{mag/1e3:.1f}kN", ha='center', fontsize=9)
for i, (mag, pos) in enumerate(moments):
    direction = np.sign(mag)
    axs[4].arrow(pos, 0.8, 0.5 * direction, 0, head_width=0.2, head_length=0.2, fc='orange', ec='orange')
    axs[4].text(pos, 1.0, f"{mag/1e3:.1f}kNm", ha='center', fontsize=9, color='orange')
if use_udl:
    axs[4].fill_between(x_vals, 0.2, 0.8, where=(x_vals >= a_udl) & (x_vals <= b_udl), color='orange', alpha=0.4)
    axs[4].text((a_udl + b_udl)/2, 0.9, f"{w/1e3:.1f}kN/m", ha='center', fontsize=9, color='orange')

st.pyplot(fig)

st.subheader("📤 Export to PDF")
if st.button("Export Current Plot to PDF"):
    with PdfPages("beam_results.pdf") as pdf:
        pdf.savefig(fig)
    with open("beam_results.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="beam_results.pdf", mime="application/pdf")

import streamlit as st

# Constants
DROPPER_VOLUME_ML = 2.5  # One drop = 2.5 mL of concentrate

def drops_needed(target_ppm, stock_ppm, test_volume_ml, batch_volume_ml):
    """
    Calculate how many drops are needed to achieve target ppm in the batch.
    """
    ppm_per_ml = stock_ppm / test_volume_ml
    ppm_per_drop = ppm_per_ml * DROPPER_VOLUME_ML
    total_ppm_needed = target_ppm * batch_volume_ml / 1000  # convert to mg/L over batch
    return round(total_ppm_needed / ppm_per_drop, 2)

st.title("💧 Brew Water Drop Calculator (TDS Accurate)")

# Default volumes
test_volume_ml = st.number_input("PPM Test Volume (mL) (e.g. 50 mL)", value=50.0)
batch_volume_ml = st.number_input("Target Batch Size (mL)", value=500.0)

st.write("---")
st.subheader("Enter PPM per 50 mL (your concentrates):")
stock_ppm = {}
minerals = ["Magnesium (Mg)", "Chloride (Cl)", "Sodium (Na)", "KHCO₃ (KH)"]
default_stock_ppm = {
    "Magnesium (Mg)": 100,
    "Chloride (Cl)": 200,
    "Sodium (Na)": 65,
    "KHCO₃ (KH)": 75
}
for m in minerals:
    stock_ppm[m] = st.number_input(f"{m} PPM in {test_volume_ml} mL", value=default_stock_ppm[m])

st.write("---")
st.subheader("Enter Target PPMs for Final Water:")
target_ppm = {}
default_target_ppm = {
    "Magnesium (Mg)": 40,
    "Chloride (Cl)": 40,
    "Sodium (Na)": 10,
    "KHCO₃ (KH)": 25
}
for m in minerals:
    target_ppm[m] = st.number_input(f"Target {m} (ppm)", value=default_target_ppm[m])

if st.button("Calculate"):
    st.write("## 🧮 Drop Results")
    total_tds = 0
    for m i

import streamlit as st

# Constants
DROPPER_VOLUME_ML = 2.5  # One drop = 2.5 mL of concentrate

def drops_needed(target_ppm, stock_ppm, test_volume_ml, batch_volume_ml):
    """
    Calculate how many drops are needed to achieve target ppm in the batch.
    """
    if stock_ppm == 0 or test_volume_ml == 0:
        return 0, 0

    ppm_per_ml = stock_ppm / test_volume_ml
    ppm_per_drop = ppm_per_ml * DROPPER_VOLUME_ML

    # Total mg of mineral needed = target_ppm × (batch_L)
    total_mg_needed = target_ppm * (batch_volume_ml / 1000)
    drops = total_mg_needed / ppm_per_drop

    # Actual ppm in batch = drops × ppm_per_drop / batch_L
    actual_ppm = (drops * ppm_per_drop) / (batch_volume_ml / 1000)

    return round(drops, 2), round(actual_ppm, 2)

st.title("💧 Brew Water Drop Calculator")

# Volume inputs
test_volume_ml = st.number_input("Volume used to test ppm (mL, e.g. 50)", value=50.0, min_value=1.0)
batch_volume_ml = st.number_input("Final batch volume (mL, e.g. 500)", value=500.0, min_value=1.0)

# Minerals
minerals = ["Magnesium (Mg)", "Chloride (Cl)", "Sodium (Na)", "KHCO₃ (KH)"]
default_stock_ppm = {
    "Magnesium (Mg)": 100.0,
    "Chloride (Cl)": 200.0,
    "Sodium (Na)": 65.0,
    "KHCO₃ (KH)": 75.0
}
default_target_ppm = {
    "Magnesium (Mg)": 40.0,
    "Chloride (Cl)": 40.0,
    "Sodium (Na)": 10.0,
    "KHCO₃ (KH)": 25.0
}

st.header("📥 Concentrate PPM (in test volume)")
stock_ppm = {}
for mineral in minerals:
    stock_ppm[mineral] = st.number_input(f"{mineral} PPM", value=default_stock_ppm[mineral], key=f"stock_{mineral}")

st.header("🎯 Target PPM for Final Water")
target_ppm = {}
for mineral in minerals:
    target_ppm[mineral] = st.number_input(f"Target {mineral} (ppm)", value=default_target_ppm[mineral], key=f"target_{mineral}")

if st.button("Calculate Drops"):
    st.subheader("🧮 Drop Count & Final PPM")
    total_tds = 0
    for mineral in minerals:
        drops, actual = drops_needed(
            target_ppm[mineral],
            stock_ppm[mineral],
            test_volume_ml,
            batch_volume_ml
        )
        total_tds += actual
        st.write(f"**{mineral}**: {drops} drops → ~{actual} ppm")

    st.markdown(f"### ✅ Estimated Total TDS: `{round(total_tds, 1)} ppm`")

import streamlit as st

def calculate_drops(measured_ppm, test_volume_ml, batch_volume_ml, target_ppm):
    if measured_ppm == 0:
        return 0
    # ppm per mL of concentrate
    ppm_per_ml_concentrate = measured_ppm / test_volume_ml
    # ppm contribution from 1 drop in final batch
    ppm_per_drop_in_batch = ppm_per_ml_concentrate / batch_volume_ml
    # number of drops needed to reach target ppm
    return round(target_ppm / ppm_per_drop_in_batch, 2)

st.title("PPM Drop Calculator with TDS")

# Default volumes
default_test_volume = 50.0
default_batch_volume = 500.0

test_volume_ml = st.number_input("Test volume for 1 drop (mL)", min_value=1.0, value=default_test_volume)
batch_volume_ml = st.number_input("Batch volume to prepare (mL)", min_value=1.0, value=default_batch_volume)

minerals = ["Magnesium (Mg)", "Calcium (Ca)", "Sodium (Na)", "KHCO₃ (KH)"]

default_measured_ppm = {
    "Magnesium (Mg)": 100.0,
    "Calcium (Ca)": 200.0,
    "Sodium (Na)": 65.0,
    "KHCO₃ (KH)": 75.0
}

default_target_ppm = {
    "Magnesium (Mg)": 40.0,
    "Calcium (Ca)": 40.0,
    "Sodium (Na)": 20.0,
    "KHCO₃ (KH)": 25.0
}

# Inputs
st.header("Measured PPM of 1 drop in test volume")
measured_ppm = {mineral: st.number_input(
    mineral,
    min_value=0.0,
    value=default_measured_ppm[mineral],
    key=f"measured_{mineral}"
) for mineral in minerals}

st.header("Target PPM in final batch")
target_ppm = {mineral: st.number_input(
    mineral,
    min_value=0.0,
    value=default_target_ppm[mineral],
    key=f"target_{mineral}"
) for mineral in minerals}

if st.button("Calculate"):
    drops_needed = {}
    actual_ppm = {}
    total_tds = 0.0

    st.subheader("💧 Drops Needed:")
    for mineral in minerals:
        drops = calculate_drops(
            measured_ppm[mineral],
            test_volume_ml,
            batch_volume_ml,
            target_ppm[mineral]
        )
        drops_needed[mineral] = drops
        st.write(f"{mineral}: {drops} drops")

    st.subheader("📊 Actual PPM in Final Batch:")
    for mineral in minerals:
        ppm_per_ml_concentrate = measured_ppm[mineral] / test_volume_ml
        ppm_per_drop_in_batch = ppm_per_ml_concentrate / batch_volume_ml
        ppm_in_batch = ppm_per_drop_in_batch * drops_needed[mineral]
        actual_ppm[mineral] = ppm_in_batch
        total_tds += ppm_in_batch
        st.write(f"{mineral}: {ppm_in_batch:.2f} ppm")

    st.subheader(f"🔬 Total Estimated TDS: {total_tds:.2f} ppm")

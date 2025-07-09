import streamlit as st

def calculate_drops(measured_ppm, test_volume_ml, batch_volume_ml, target_ppm):
    if measured_ppm == 0:
        return 0
    ppm_per_drop = measured_ppm / test_volume_ml  # ppm per 1 mL of concentrate
    ppm_per_drop_in_batch = ppm_per_drop * 2.5 / batch_volume_ml  # 2.5 mL per drop
    return round(target_ppm / ppm_per_drop_in_batch, 2)

st.title("PPM Drop Calculator with TDS")

# Preset default volumes
default_test_volume = 50.0   # typically how 1 drop is measured
default_batch_volume = 500.0 # your brew water size

test_volume_ml = st.number_input("Test volume for 1 drop (mL)", min_value=1.0, value=default_test_volume)
batch_volume_ml = st.number_input("Batch volume to prepare (mL)", min_value=1.0, value=default_batch_volume)

minerals = ["Magnesium (Mg)", "Chloride (Cl)", "Sodium (Na)", "KHCO₃ (KH)"]

default_measured_ppm = {
    "Magnesium (Mg)": 100.0,
    "Chloride (Cl)": 200.0,
    "Sodium (Na)": 65.0,
    "KHCO₃ (KH)": 75.0
}

default_target_ppm = {
    "Magnesium (Mg)": 40.0,
    "Chloride (Cl)": 40.0,
    "Sodium (Na)": 20.0,
    "KHCO₃ (KH)": 25.0
}

st.header("Measured PPM of 1 drop in test volume")
measured_ppm = {}
for mineral in minerals:
    measured_ppm[mineral] = st.number_input(
        f"{mineral}",
        min_value=0.0,
        value=default_measured_ppm[mineral],
        key=f"measured_{mineral}"
    )

st.header("Target PPM in final batch")
target_ppm = {}
for mineral in minerals:
    target_ppm[mineral] = st.number_input(
        f"{mineral}",
        min_value=0.0,
        value=default_target_ppm[mineral],
        key=f"target_{mineral}"
    )

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
        ppm_per_ml = measured_ppm[mineral] / test_volume_ml
        ppm_per_drop = ppm_per_ml * 2.5
        total_ppm = ppm_per_drop * drops_needed[mineral] / batch_volume_ml
        actual_ppm[mineral] = total_ppm
        total_tds += total_ppm
        st.write(f"{mineral}: {total_ppm:.2f} ppm")

    st.subheader(f"🔬 Total Estimated TDS: {total_tds:.2f} ppm")

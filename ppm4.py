import streamlit as st

def calculate_drops(measured_ppm, test_volume_ml, batch_volume_ml, target_ppm):
    # Basic validation
    if measured_ppm <= 0 or test_volume_ml <= 0 or batch_volume_ml <= 0:
        return 0.0
    # ppm contribution to the final batch from 1 measured drop:
    # ppm_per_drop_in_batch = measured_ppm * (test_volume_ml / batch_volume_ml)
    ppm_per_drop_in_batch = measured_ppm * (test_volume_ml / batch_volume_ml)
    if ppm_per_drop_in_batch == 0:
        return 0.0
    # exact number of drops (not rounded)
    return target_ppm / ppm_per_drop_in_batch

st.title("PPM Drop Calculator with TDS (fixed logic)")

# Preset default volumes (mL)
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

    st.subheader("💧 Drops Needed (exact, shown rounded):")
    for mineral in minerals:
        exact_drops = calculate_drops(
            measured_ppm[mineral],
            test_volume_ml,
            batch_volume_ml,
            target_ppm[mineral]
        )
        drops_needed[mineral] = exact_drops
        st.write(f"{mineral}: {exact_drops:.2f} drops")

    st.subheader("📊 Actual PPM in Final Batch (from the computed drops):")
    for mineral in minerals:
        ppm_per_drop_in_batch = measured_ppm[mineral] * (test_volume_ml / batch_volume_ml)
        ppm_in_batch = ppm_per_drop_in_batch * drops_needed[mineral]
        actual_ppm[mineral] = ppm_in_batch
        total_tds += ppm_in_batch
        st.write(f"{mineral}: {ppm_in_batch:.2f} ppm (target: {target_ppm[mineral]:.2f} ppm)")

    st.subheader(f"🔬 Total Estimated TDS: {total_tds:.2f} ppm")

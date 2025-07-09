import streamlit as st

def calculate_drops(measured_ppm, test_volume_ml, target_ppm, batch_volume_ml):
    if measured_ppm == 0:
        return 0
    ppm_per_drop_per_ml = measured_ppm / test_volume_ml
    ppm_per_drop_in_batch = ppm_per_drop_per_ml * batch_volume_ml
    return round(target_ppm / ppm_per_drop_in_batch, 2)

st.title("PPM Drop Calculator")

# Preset default volumes
default_batch_volume = 50.0
default_test_volume = 500.0

test_volume_ml = st.number_input("Volume used to test 1 drop (mL)", min_value=1.0, value=default_batch_volume)
batch_volume_ml = st.number_input("Batch volume (mL)", min_value=1.0, value=default_test_volume)

minerals = ["Magnesium (Mg)", "Chloride (Cl)", "Sodium (Na)", "KHCO₃ (KH)"]

# Preset ppm defaults for each mineral
default_measured_ppm = {
    "Magnesium (Mg)": 90.0,
    "Chloride (Cl)": 195.0,
    "Sodium (Na)": 66.0,
    "KHCO₃ (KH)": 75.0
}

default_target_ppm = {
    "Magnesium (Mg)": 35.0,
    "Chloride (Cl)": 35.0,
    "Sodium (Na)": 10.0,
    "KHCO₃ (KH)": 10.0
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

st.header("Target PPM in batch volume")
target_ppm = {}
for mineral in minerals:
    target_ppm[mineral] = st.number_input(
        f"{mineral}",
        min_value=0.0,
        value=default_target_ppm[mineral],
        key=f"target_{mineral}"
    )

if st.button("Calculate Drops Needed"):
    st.write("### Drops to Add:")
    drops_dict = {}
    for mineral in minerals:
        drops = calculate_drops(
            measured_ppm[mineral],
            batch_volume_ml,
            target_ppm[mineral],
            test_volume_ml
        )
        drops_dict[mineral] = drops
        st.write(f"{mineral}: {drops} drops")

    st.write("### Actual PPM in Final Batch:")
    total_ppm = 0
    for mineral in minerals:
        ppm_per_drop = (measured_ppm[mineral] / test_volume_ml) * batch_volume_ml
        actual_ppm = ppm_per_drop * drops_dict[mineral]
        total_ppm += actual_ppm
        st.write(f"{mineral}: {actual_ppm:.2f} ppm")

    st.write(f"### Total Estimated TDS: {total_ppm:.2f} ppm")

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Halaman utama
st.title("Kalkulator Antioksidan DPPH")
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Halaman Utama", "Input Data", "Hasil Perhitungan"])

if page == "Halaman Utama":
    st.header("Selamat Datang")
    st.write("Gunakan aplikasi ini untuk menghitung nilai IC50 berdasarkan uji DPPH.")
elif page == "Input Data":
    st.header("Input Data Uji DPPH")
    
    # Input Blanko
    blank_abs = st.number_input("Masukkan nilai absorbansi blanko (A):", min_value=0.0, step=0.01)
    
    # Input Deret Konsentrasi
    concentrations_input = st.text_area("Masukkan deret konsentrasi (pisahkan dengan koma):", value="10, 20, 30, 40, 50")
    absorbances_input = st.text_area("Masukkan deret absorbansi (sesuai konsentrasi, pisahkan dengan koma):", value="0.5, 0.4, 0.3, 0.2, 0.1")
    
    if st.button("Simpan Data"):
        try:
            concentrations = np.array([float(x) for x in concentrations_input.split(",")])
            absorbances = np.array([float(x) for x in absorbances_input.split(",")])
            
            if len(concentrations) != len(absorbances):
                st.error("Jumlah konsentrasi dan absorbansi harus sama.")
            else:
                st.session_state['blank_abs'] = blank_abs
                st.session_state['concentrations'] = concentrations
                st.session_state['absorbances'] = absorbances
                st.success("Data berhasil disimpan.")
        except ValueError:
            st.error("Masukkan angka valid untuk konsentrasi dan absorbansi.")
elif page == "Hasil Perhitungan":
    st.header("Hasil Perhitungan")
    if 'concentrations' in st.session_state and 'absorbances' in st.session_state:
        blank_abs = st.session_state['blank_abs']
        concentrations = st.session_state['concentrations']
        absorbances = st.session_state['absorbances']
        
        # Hitung % inhibisi
        inhibition = ((blank_abs - absorbances) / blank_abs) * 100
        
        # Tabel hasil
        data = pd.DataFrame({
            "Konsentrasi (µg/mL)": concentrations,
            "% Inhibisi": inhibition
        })
        st.table(data)
        
        # Plot
        x = concentrations.reshape(-1, 1)
        y = inhibition
        model = LinearRegression()
        model.fit(x, y)
        y_pred = model.predict(x)
        
        st.subheader("Kurva Konsentrasi vs % Inhibisi")
        plt.figure(figsize=(8, 5))
        plt.scatter(concentrations, inhibition, color="blue", label="Data Asli")
        plt.plot(concentrations, y_pred, color="red", label="Regresi Linear")
        plt.xlabel("Konsentrasi (µg/mL)")
        plt.ylabel("% Inhibisi")
        plt.title("Kurva Regresi Linear")
        plt.legend()
        st.pyplot(plt)
        
        # Hasil regresi
        slope = model.coef_[0]
        intercept = model.intercept_
        ic50 = (50 - intercept) / slope
        
        st.write(f"Persamaan Regresi: y = {slope:.4f}x + {intercept:.4f}")
        st.write(f"Nilai IC50: {ic50:.2f} µg/mL")
        
        if ic50 > 200:
            st.write("Interpretasi IC50: Sangat Lemah")
        elif ic50 > 100:
            st.write("Interpretasi IC50: Lemah")
        elif ic50 > 50:
            st.write("Interpretasi IC50: Kuat")
        else:
            st.write("Interpretasi IC50: Sangat Kuat")
    else:
        st.warning("Data belum dimasukkan. Kembali ke halaman Input Data.")

"""
NGC 6505 Einstein Ring — τ Framework Prediction vs Observation
==============================================================
Data source: O'Riordan et al. 2025, A&A 694, A145 (Euclid)
             arXiv:2502.06505

τ framework: Paper III (dark-matter-running-g)
Formula: G(r) = G_N [1 + 2 k_* r / π],  k_* ≈ 2.7 × 10⁻² kpc⁻¹
"""

import numpy as np

print("=" * 70)
print("NGC 6505 Einstein Ring: τ Framework vs Observation")
print("=" * 70)

# ========================================
# Observed data (Euclid, O'Riordan+2025)
# ========================================
z_lens = 0.042          # lens redshift
z_source = 0.4058       # source redshift
theta_E = 2.500         # Einstein radius [arcsec]
R_Ein_kpc = 2.1         # Einstein radius [kpc] (physical, at lens)
M_Ein = 1.53e11         # total lensing mass within R_Ein [M_sun]
M_star_Chab = 1.06e11   # stellar mass (Chabrier IMF) [M_sun]
M_star_model = 1.36e11  # stellar mass (lensing+dynamics fit) [M_sun]
alpha_IMF = 1.26        # IMF mismatch: M_star_model / M_star_Chab
f_DM_obs = 0.111        # dark matter fraction observed
f_DM_err_plus = 0.054   # +error
f_DM_err_minus = 0.035  # -error
M_DM_obs = M_Ein - M_star_model  # ~1.7e10 M_sun
sigma_v = 303           # velocity dispersion [km/s]
M_500 = 4.1e13          # NFW halo mass [M_sun]

print("\n--- Observed Data (Euclid) ---")
print(f"Lens: NGC 6505, z = {z_lens}")
print(f"Source: z = {z_source}")
print(f"Einstein radius: {theta_E}\" = {R_Ein_kpc} kpc")
print(f"Total lensing mass: {M_Ein:.2e} M_sun")
print(f"Stellar mass (Chabrier): {M_star_Chab:.2e} M_sun")
print(f"Stellar mass (model): {M_star_model:.2e} M_sun")
print(f"α_IMF = {alpha_IMF}")
print(f"Dark matter fraction: {f_DM_obs*100:.1f}% (+{f_DM_err_plus*100:.1f}/-{f_DM_err_minus*100:.1f})")
print(f"Dark matter mass: {M_DM_obs:.2e} M_sun")
print(f"σ_v = {sigma_v} km/s")
print(f"M_500 (NFW halo) = {M_500:.2e} M_sun")

# ========================================
# τ Framework Prediction (Paper III)
# ========================================
# Running G: G(r)/G_N = 1 + 2 k_* r / π
# k_* from SPARC galaxies (Kumar 2025, Gubitosi+2024)

k_star = 2.7e-2   # [kpc^-1] — universal crossover scale
r_c = 1 / k_star   # crossover radius [kpc]

print("\n--- τ Framework Parameters ---")
print(f"k_* = {k_star} kpc⁻¹ (universal crossover scale)")
print(f"Crossover radius r_c = 1/k_* = {r_c:.1f} kpc")

# G_eff at Einstein radius
G_ratio = 1 + 2 * k_star * R_Ein_kpc / np.pi
print(f"\nG(R_Ein)/G_N = 1 + 2×{k_star}×{R_Ein_kpc}/π = {G_ratio:.4f}")

# Apparent dark matter fraction from running G
f_DM_tau = 1 - 1/G_ratio
M_DM_tau = M_star_model * (G_ratio - 1)

print(f"\n--- τ Framework Prediction ---")
print(f"f_DM (running G) = {f_DM_tau*100:.2f}%")
print(f"M_DM (apparent)  = {M_DM_tau:.2e} M_sun")

# Check the de Sitter term
c_light = 3e5     # km/s
H_0 = 67.8        # km/s/Mpc
L_dS = c_light / H_0 * 1e3  # in kpc
dS_ratio = R_Ein_kpc / L_dS
print(f"\nde Sitter scale: L_dS = c/H₀ = {L_dS:.2e} kpc")
print(f"r/L_dS = {dS_ratio:.2e} → de Sitter term negligible at 2.1 kpc")

# ========================================
# Comparison
# ========================================
print("\n" + "=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"                        τ framework    Observed")
print(f"f_DM within R_Ein:      {f_DM_tau*100:6.2f}%         {f_DM_obs*100:.1f}% (+{f_DM_err_plus*100:.1f}/-{f_DM_err_minus*100:.1f})")
print(f"M_DM within R_Ein:      {M_DM_tau:.2e}    {M_DM_obs:.2e} M_sun")

# Discrepancy
ratio = f_DM_obs / f_DM_tau
sigma_off = (f_DM_obs - f_DM_tau) / f_DM_err_minus
print(f"\nRatio observed/predicted: {ratio:.1f}×")
print(f"Discrepancy: ~{sigma_off:.1f}σ (using lower error bar)")

# ========================================
# Alternative: infer α_IMF from τ framework
# ========================================
# If all "DM" is from running G, what stellar mass is needed?
# M_Ein = M_star_true × G(R)/G_N
# → M_star_true = M_Ein / G_ratio
M_star_tau = M_Ein / G_ratio
alpha_IMF_tau = M_star_tau / M_star_Chab

print(f"\n--- Alternative: Infer IMF from τ framework ---")
print(f"If ALL lensing mass = stellar × G_eff/G_N:")
print(f"  M_star_true = M_Ein / G_ratio = {M_star_tau:.2e} M_sun")
print(f"  α_IMF = {alpha_IMF_tau:.2f} (Chabrier = 1.0, Salpeter ≈ 1.7)")
print(f"  Compare: Euclid fitted α_IMF = {alpha_IMF}")
print(f"  Difference: {(alpha_IMF_tau - alpha_IMF)/alpha_IMF * 100:.1f}%")
print(f"  → τ framework requires a ~10% heavier IMF, still well within")
print(f"    the allowed range between Chabrier and Salpeter")

# ========================================
# G(r)/G_N at various radii (Paper III predictions)
# ========================================
print("\n--- G(r)/G_N Predictions at Various Radii ---")
radii = [0.1, 1, 2.1, 5, 10, 37, 50, 100, 200]
print(f"{'r [kpc]':>10} {'G/G_N':>10} {'f_DM_apparent':>15} {'M_DM/M_bar':>12}")
for r in radii:
    G_r = 1 + 2 * k_star * r / np.pi
    f_dm = 1 - 1/G_r
    m_ratio = G_r - 1
    marker = " ← R_Ein" if r == 2.1 else ""
    print(f"{r:10.1f} {G_r:10.4f} {f_dm*100:14.2f}% {m_ratio:11.4f}{marker}")

# ========================================
# Physical interpretation
# ========================================
print("\n" + "=" * 70)
print("PHYSICAL INTERPRETATION (τ Framework)")
print("=" * 70)
print("""
In the τ framework, there are NO dark matter particles in NGC 6505.

What Euclid measures as "dark matter" is the combined effect of:

1. RUNNING G (η = 1):
   At r = 2.1 kpc, the effective gravitational coupling is
   G_eff/G_N = {:.4f} (a {:.1f}% enhancement).
   This creates an apparent mass excess of {:.2e} M_sun,
   accounting for ~{:.0f}% of the observed "dark matter."

2. IMF UNCERTAINTY:
   The remaining discrepancy (~{:.0f}%) is absorbed by a slightly
   heavier stellar IMF: α_IMF ≈ {:.2f} instead of {:.2f}.
   This is well within the known IMF uncertainty range
   (Chabrier = 1.0, Kroupa ≈ 1.1, Salpeter ≈ 1.7).

3. WHY THE DM FRACTION IS SO SMALL (11%):
   In the NFW picture, massive elliptical galaxies have very low
   DM fractions in their centers because baryons dominate.
   In the τ framework, this is naturally explained: running G
   corrections are small at small radii (2k_*r/π ≈ {:.1f}%),
   growing only at galactic scales (r > 37 kpc).

KEY PREDICTION:
   If the Euclid team (or JWST follow-up) measures the mass
   profile at larger radii (10-100 kpc), the τ framework
   predicts G/G_N = 1.17 at 10 kpc and 2.72 at 100 kpc —
   much more dark matter than NFW at large r (no cutoff).
""".format(
    G_ratio, (G_ratio-1)*100, M_DM_tau, f_DM_tau/f_DM_obs*100,
    (1 - f_DM_tau/f_DM_obs)*100, alpha_IMF_tau, alpha_IMF,
    (G_ratio-1)*100
))

# ========================================
# Σ_total decomposition at R_Ein
# ========================================
G_N_cgs = 6.674e-8    # cm³ g⁻¹ s⁻²
M_sun_g = 1.989e33     # g
kpc_cm = 3.086e21       # cm
c_cgs = 2.998e10        # cm/s

M_bar_g = M_star_model * M_sun_g
r_s_cm = 2 * G_N_cgs * M_bar_g / c_cgs**2
r_s_kpc = r_s_cm / kpc_cm

r_cm = R_Ein_kpc * kpc_cm

Sigma_Newton = r_s_kpc / R_Ein_kpc
Sigma_running = 2 * k_star * r_s_kpc / np.pi * np.log(R_Ein_kpc / r_c)

print("--- Σ_total Decomposition at R_Ein ---")
print(f"Schwarzschild radius: r_s = {r_s_kpc:.4e} kpc")
print(f"Σ_Newton = r_s/r = {Sigma_Newton:.4e}")
print(f"Σ_running ≈ (2k_*r_s/π) ln(r/r_c) = {Sigma_running:.4e}")
print(f"Σ_deSitter ≈ β r/L_dS ≈ negligible")
print(f"\nτ_Newton = 1 - exp(-Σ_Newton/2) ≈ {Sigma_Newton/2:.4e}")
print(f"τ_total ≈ {(Sigma_Newton + abs(Sigma_running))/2:.4e}")
print(f"\nNote: Σ values are tiny because R_Ein >> r_s.")
print(f"The 'dark matter' effect comes from the running of G,")
print(f"not from large Σ — it's the RATIO G_eff/G_N that matters.")

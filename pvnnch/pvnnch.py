import numpy as np
from astropy.table import Table

def nn2vec(flux, flux_err, mjd, science_name, template_name):
    flux = np.array(flux)
    flux_err = np.array(flux_err)
    mjd = np.array(mjd)
    science_name = np.array(science_name)
    template_name = np.array(template_name)

    mask = ~np.isnan(flux_err)
    df = df_[mask]
    
    vec_mjd = np.unique(mjd[mask])
    
    sciences = np.unique(science_name)
    templates = np.unique(template_name)
    templates = np.array([t for t in templates if t not in sciences])
    df.set_index(['science_name', 'template_name'], inplace=True)
    
    NS = len(sciences)
    NT = len(templates)
    A_ST = np.zeros(NS * NT)
    C_ST = np.zeros(NS * NT)
    for i, s in enumerate(sciences):
        for j, t in enumerate(templates):
            A_ST[i*NT + j] = flux[s, t]
            C_ST[i*NT + j] = flux_err[s, t]**2
    A_SS = np.zeros(int(NS * (NS - 1)/2))
    C_SS = np.zeros(int(NS * (NS - 1)/2))
    k = 0
    for i, s1 in enumerate(sciences):
        for j, s2 in enumerate(sciences):
            if j <= i:
                continue
            A_SS[k] = flux[s1, s2]
            C_SS[k] = flux_err[s1, s2]**2
            k += 1
    A = np.hstack((A_SS, A_ST))
    C = np.diag(np.hstack((C_SS, C_ST)))
    
    p = NS
    q = NT
    n = p * (p - 1) // 2
    
    # X_SS: n x p
    X_SS = np.zeros((n, p))
    k = 0
    for i in range(p):
        for j in range(p):
            if j <= i:
                continue
            X_SS[k, i] = 1
            X_SS[k, j] = -1
            k += 1
    
    # X_ST: pq x p
    X_ST = np.zeros((p * q, p))
    for i in range(p):
        for j in range(q):
            X_ST[i*q + j, i] = 1
    
    X = np.vstack((X_SS, X_ST))
    
    Xt_Cinv = X.T @ np.linalg.pinv(C)
    Cvv = np.linalg.pinv(Xt_Cinv @ X)
    V = Cvv @ Xt_Cinv @ A

    return vec_mjd, V
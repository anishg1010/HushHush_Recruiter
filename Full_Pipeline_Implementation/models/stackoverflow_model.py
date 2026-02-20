def run_stackoverflow_model(df):
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import QuantileTransformer
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression

    metadata = df[['user_id', 'DisplayName', 'Reputation']]

    X = df.select_dtypes(include=[np.number]).fillna(0)

    qt = QuantileTransformer(output_distribution='normal', random_state=42)
    X_scaled = qt.fit_transform(X)

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    kmeans = KMeans(n_clusters=2, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X_pca)

    order = df.groupby('Cluster')['Reputation'].median().sort_values().index
    mapping = {k: i for i, k in enumerate(order)}
    df['Tier'] = df['Cluster'].map(mapping)
    df['Tier_Name'] = df['Tier'].map({0: 'Standard', 1: 'Top Talent'})

    log_reg = LogisticRegression()
    log_reg.fit(X_pca, df['Tier'])

    probs = log_reg.decision_function(X_pca)
    qt_score = QuantileTransformer(output_distribution='uniform')
    scores = qt_score.fit_transform(probs.reshape(-1, 1)) * 100

    final = metadata.copy()
    final['Tier_Name'] = df['Tier_Name']
    final['SOTS'] = scores

    return final.sort_values('SOTS', ascending=False)

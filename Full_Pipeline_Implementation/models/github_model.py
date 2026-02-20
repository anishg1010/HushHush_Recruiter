def run_github_model(df):
    # ---- YOUR EXISTING CODE STARTS ----
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import QuantileTransformer, MinMaxScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    cols_to_clean = df.columns.drop(['username'])
    for col in cols_to_clean:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    cols_to_drop = ['username', 'total_stars', 'total_forks', 'total_watchers', 'total_open_issues']
    X = df.drop(columns=cols_to_drop, errors='ignore')
    X = X.select_dtypes(include=[np.number])

    scaler = QuantileTransformer(
        output_distribution='normal',
        n_quantiles=min(len(df), 500),
        random_state=42
    )
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=50)
    labels = kmeans.fit_predict(X_pca)

    def align_labels(labels, data):
        temp = pd.DataFrame({'lbl': labels, 'proxy': data['followers']})
        means = temp.groupby('lbl')['proxy'].mean().sort_values()
        mapping = {old: new for new, old in enumerate(means.index)}
        return [mapping[l] for l in labels]

    df['cluster_label'] = align_labels(labels, df)
    df['cluster_name'] = df['cluster_label'].map({0: 'Weak', 1: 'Average', 2: 'Strong'})

    y = df['cluster_label']
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    log_reg = LogisticRegression(multi_class='multinomial', max_iter=2000)
    log_reg.fit(X_train, y_train)

    probs = log_reg.decision_function(X_scaled)
    raw_scores = probs @ [0, 1, 2]

    gts_scaler = MinMaxScaler((0, 100))
    df['GTS'] = gts_scaler.fit_transform(raw_scores.reshape(-1, 1))

    result = df[['username', 'GTS', 'cluster_name']].sort_values('GTS', ascending=False)
    # ---- YOUR EXISTING CODE ENDS ----

    return result

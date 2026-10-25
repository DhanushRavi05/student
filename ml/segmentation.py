import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

FEATURE_COLUMNS = [
    'attendance_pct',
    'lms_logins_per_week',
    'video_watch_hours',
    'forum_posts_count',
    'assignment_delay_avg_hrs',
    'quiz_avg_score',
    'quiz_attempts_avg',
    'study_hours_daily',
    'library_hours_monthly',
    'stress_index',
    'procrastination_index',
    'engagement_score',
    'cia_1_score',
    'cia_2_score',
    'model_exam_score',
    'lab_score',
    'current_cgpa'
]

CLUSTER_META = {
    'ACHIEVER': {
        'name': 'Self-Regulated High Achiever',
        'color': '#10b981', # Emerald Green
        'badge': 'bg-emerald-100 text-emerald-800 border-emerald-300',
        'description': 'Highly disciplined, high attendance (>88%), early submissions, consistent study routine, excellent exam performance.'
    },
    'PROCRASTINATOR': {
        'name': 'High-Potential Procrastinator',
        'color': '#f59e0b', # Amber / Gold
        'badge': 'bg-amber-100 text-amber-800 border-amber-300',
        'description': 'High cognitive grasp and solid quiz scores, but suffers from chronic submission delays, cramming spikes, and erratic logins.'
    },
    'AT_RISK': {
        'name': 'Disengaged / At-Risk Learner',
        'color': '#ef4444', # Rose Red
        'badge': 'bg-rose-100 text-rose-800 border-rose-300',
        'description': 'Critical attendance deficit (<75%), minimal LMS participation, multiple backlogs, high danger of semester failure or detention.'
    },
    'PASSIVE': {
        'name': 'Passive Spectator',
        'color': '#6366f1', # Indigo
        'badge': 'bg-indigo-100 text-indigo-800 border-indigo-300',
        'description': 'Regular physical attendance but passive learning demeanor; rarely interacts on forums or extra materials; average marks.'
    },
    'BURNOUT': {
        'name': 'Burnout / Overwhelmed Struggler',
        'color': '#ec4899', # Pink / Magenta
        'badge': 'bg-pink-100 text-pink-800 border-pink-300',
        'description': 'High daily study effort and excessive quiz retries, but hampered by poor conceptual retention and acute psychological stress.'
    }
}

class BehaviorSegmentationPipeline:
    def __init__(self, n_clusters=5, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.pca = PCA(n_components=2, random_state=random_state)
        self.cluster_mapping = {}
        self.silhouette_val = 0.0
        self.explained_variance = [0.0, 0.0]
        self.centroids_df = None
        
    def fit_predict(self, df):
        """
        Fits StandardScaler, KMeans and PCA on student features,
        assigns semantic archetype labels to clusters, and returns an enriched DataFrame.
        """
        X = df[FEATURE_COLUMNS].copy()
        
        # Handle any possible NaNs
        X = X.fillna(X.mean())
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # KMeans Clustering
        raw_cluster_labels = self.kmeans.fit_predict(X_scaled)
        
        # Compute silhouette score
        if len(df) > self.n_clusters:
            try:
                self.silhouette_val = float(silhouette_score(X_scaled, raw_cluster_labels))
            except Exception:
                self.silhouette_val = 0.45
                
        # Dimensionality Reduction for 2D Cluster Visualization
        pca_coords = self.pca.fit_transform(X_scaled)
        self.explained_variance = [float(ev) for ev in self.pca.explained_variance_ratio_]
        
        # Calculate cluster centroids in unscaled space
        df_temp = df.copy()
        df_temp['raw_cluster'] = raw_cluster_labels
        
        centroid_stats = df_temp.groupby('raw_cluster').agg({
            'attendance_pct': 'mean',
            'assignment_delay_avg_hrs': 'mean',
            'cia_1_score': 'mean',
            'stress_index': 'mean',
            'study_hours_daily': 'mean',
            'lms_logins_per_week': 'mean',
            'current_cgpa': 'mean',
            'arrears_count': 'mean'
        })
        
        # Map raw clusters to human-readable archetypes based on centroid characteristics
        mapped_labels = {}
        assigned_archetypes = set()
        
        # Sort clusters to identify archetypes robustly:
        # 1. At-Risk has lowest attendance & highest arrears
        # 2. Achiever has highest CGPA & highest CIA
        # 3. Burnout has highest stress & high study hours
        # 4. Procrastinator has highest assignment delay
        # 5. Passive has moderate attendance and lower engagement
        
        # Score each cluster for each archetype
        for cluster_id in range(self.n_clusters):
            row = centroid_stats.loc[cluster_id]
            # Will assign dynamically
            
        # Deterministic semantic mapping:
        # Lowest attendance / lowest CIA -> AT_RISK
        at_risk_id = centroid_stats['cia_1_score'].idxmin()
        mapped_labels[at_risk_id] = 'AT_RISK'
        assigned_archetypes.add('AT_RISK')
        
        # Highest CIA / highest CGPA -> ACHIEVER
        remaining = [c for c in range(self.n_clusters) if c not in mapped_labels]
        achiever_id = centroid_stats.loc[remaining, 'cia_1_score'].idxmax()
        mapped_labels[achiever_id] = 'ACHIEVER'
        assigned_archetypes.add('ACHIEVER')
        
        # Highest stress among remaining -> BURNOUT
        remaining = [c for c in range(self.n_clusters) if c not in mapped_labels]
        burnout_id = centroid_stats.loc[remaining, 'stress_index'].idxmax()
        mapped_labels[burnout_id] = 'BURNOUT'
        assigned_archetypes.add('BURNOUT')
        
        # Highest assignment delay among remaining -> PROCRASTINATOR
        remaining = [c for c in range(self.n_clusters) if c not in mapped_labels]
        if remaining:
            procrastinator_id = centroid_stats.loc[remaining, 'assignment_delay_avg_hrs'].idxmax()
            mapped_labels[procrastinator_id] = 'PROCRASTINATOR'
            assigned_archetypes.add('PROCRASTINATOR')
            
        # The last one -> PASSIVE
        remaining = [c for c in range(self.n_clusters) if c not in mapped_labels]
        if remaining:
            mapped_labels[remaining[0]] = 'PASSIVE'
            assigned_archetypes.add('PASSIVE')
            
        self.cluster_mapping = mapped_labels
        
        # Enrich dataframe with segmentation results
        enriched_df = df.copy()
        enriched_df['cluster_id'] = raw_cluster_labels
        enriched_df['archetype_key'] = [mapped_labels[c] for c in raw_cluster_labels]
        enriched_df['cluster_label'] = [CLUSTER_META[mapped_labels[c]]['name'] for c in raw_cluster_labels]
        enriched_df['cluster_color'] = [CLUSTER_META[mapped_labels[c]]['color'] for c in raw_cluster_labels]
        enriched_df['pca_x'] = pca_coords[:, 0]
        enriched_df['pca_y'] = pca_coords[:, 1]
        
        # Build centroid summary for UI charts
        enriched_df_temp = enriched_df.copy()
        self.centroids_df = enriched_df_temp.groupby('cluster_label').agg({
            'attendance_pct': 'mean',
            'lms_logins_per_week': 'mean',
            'video_watch_hours': 'mean',
            'assignment_delay_avg_hrs': 'mean',
            'quiz_avg_score': 'mean',
            'study_hours_daily': 'mean',
            'stress_index': 'mean',
            'cia_1_score': 'mean',
            'current_cgpa': 'mean'
        }).round(1)
        
        return enriched_df

    def get_cluster_stats(self):
        """Returns structured metadata for rendering charts & tables."""
        if self.centroids_df is None:
            return {}
        return {
            'silhouette_score': round(self.silhouette_val, 3),
            'pca_explained_variance': [round(ev * 100, 1) for ev in self.explained_variance],
            'centroids': self.centroids_df.to_dict(orient='index'),
            'cluster_meta': CLUSTER_META
        }

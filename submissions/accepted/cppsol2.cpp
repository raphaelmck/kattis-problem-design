#include <bits/stdc++.h>
using namespace std;

using ll = long long;
ll INF = LLONG_MAX; 

// Represents a weighted directed edge in our adjacency list
struct Edge {
    int to;
    ll weight;
};

/*
  =====================================================
  Multi-Source BFS for Tree Distances
  Optimized for small subsets of nodes (K <= 18)
  =====================================================
*/

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k, s;
    if (!(cin >> n >> k >> s)) return 0;
    s--; // convert to 0-based indexing for internal array logic

    // Weighted adjacency list representing the museum layout (a tree)
    vector<vector<Edge>> adj(n);
    
    // Read tree edges
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        --u;
        --v;

        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }

    // room[i] = location of alarm i
    vector<int> room(k);
    vector<ll> a(k), d(k);
    for (int i = 0; i < k; i++) {
        cin >> room[i] >> a[i] >> d[i];
        room[i]--;
    }

    // No alarms => total time is 0
    if (k == 0) {
        cout << 0 << "\n";
        return 0;
    }

    // Standard BFS to compute shortest path distances from a given starting node.
    // Since the graph is a tree, a simple queue guarantees shortest paths.
    auto get_distances = [&](int start_node) {
        vector<ll> dist(n, -1);
        
        // Fast queue implementation using a vector to avoid std::queue overhead
        vector<int> q; 
        q.reserve(n);
        
        q.push_back(start_node);
        dist[start_node] = 0;
        int head = 0;
        
        while (head < (int)q.size()) {
            int u = q[head++];
            for (const auto& edge : adj[u]) {
                if (dist[edge.to] == -1) {
                    dist[edge.to] = dist[u] + edge.weight;
                    q.push_back(edge.to);
                }
            }
        }
        return dist;
    };

    // distStart[i] = distance from the guard's starting room (s) to every other room
    vector<ll> distStart = get_distances(s);
    
    // distAlarm[i][j] = distance from alarm i's room to all other rooms in the tree
    vector<vector<ll>> distAlarm(k);
    for (int i = 0; i < k; i++) {
        distAlarm[i] = get_distances(room[i]);
    }

    // FULL mask represents all K alarms being visited
    int FULL = 1 << k;
    
    // dp[mask][i] = minimum time to visit a subset of alarms (mask) ending at alarm i
    vector<vector<ll>> dp(FULL, vector<ll>(k, INF));

    // Base case: visit exactly one alarm directly from the start room
    for (int i = 0; i < k; i++) {
        ll t = distStart[room[i]] + a[i];
        if (t <= d[i]) {
            dp[1 << i][i] = t;
        }
    }

    // Transition: from the current subset of alarms, try moving to an unvisited alarm j
    for (int mask = 1; mask < FULL; mask++) {
        for (int i = 0; i < k; i++) {
            // Skip if alarm i is not in the current subset, or if this state is unreachable
            if (!(mask & (1 << i))) continue;
            if (dp[mask][i] == INF) continue;

            for (int j = 0; j < k; j++) {
                // Skip if alarm j has already been visited
                if (mask & (1 << j)) continue; 

                // nt = time finished with mask + travel from alarm i to j + time to process j
                ll nt = dp[mask][i] + distAlarm[i][room[j]] + a[j];
                
                // If we can process alarm j before its deadline, update the DP table
                if (nt <= d[j]) {
                    int next_mask = mask | (1 << j);
                    dp[next_mask][j] = min(dp[next_mask][j], nt);
                }
            }
        }
    }

    // Final answer = minimum finishing time among all valid paths that visited all K alarms
    ll ans = INF;
    for (int i = 0; i < k; i++) {
        ans = min(ans, dp[FULL - 1][i]);
    }

    if (ans == INF) {
        cout << "IMPOSSIBLE\n";
    } else {
        cout << ans << "\n";
    }

    return 0;
}

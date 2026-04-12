/*
This is a brute-force TLE solution.

It precomputes the distances correctly using BFS, but instead of using
Dynamic Programming to find the optimal path in O(K^2 * 2^K) time, 
it tests all K! possible permutations of visiting the alarms.

For K = 18, 18! is approximately 6.4 * 10^15, which will drastically 
exceed the time limit
*/

#include <bits/stdc++.h>
using namespace std;

using ll = long long;
const ll INF = LLONG_MAX;

struct Edge {
    int to;
    ll weight;
};

int main() {
    // Standard I/O optimization
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k, s;
    if (!(cin >> n >> k >> s)) return 0;
    s--; // Convert to 0-based indexing

    vector<vector<Edge>> adj(n);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        u--; v--;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }

    vector<int> room(k);
    vector<ll> a(k), d(k);
    for (int i = 0; i < k; i++) {
        cin >> room[i] >> a[i] >> d[i];
        room[i]--;
    }

    if (k == 0) {
        cout << 0 << "\n";
        return 0;
    }

    // BFS to precompute all tree distances
    auto get_distances = [&](int start_node) {
        vector<ll> dist(n, -1);
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

    vector<ll> distStart = get_distances(s);
    vector<vector<ll>> distAlarm(k);
    for (int i = 0; i < k; i++) {
        distAlarm[i] = get_distances(room[i]);
    }

    // =========================================================
    // TLE Logic: Check all K! permutations
    // =========================================================
    
    vector<int> p(k);
    iota(p.begin(), p.end(), 0); // Initialize with 0, 1, 2... k-1

    ll ans = INF;

    // Loop through every possible ordering of alarms
    do {
        ll current_time = 0;
        bool possible = true;

        // Travel from start 's' to the first alarm in the permutation
        int first_alarm = p[0];
        current_time += distStart[room[first_alarm]] + a[first_alarm];
        
        if (current_time > d[first_alarm]) {
            possible = false;
        }

        // Travel sequentially through the rest of the permutation
        for (int i = 1; i < k && possible; i++) {
            int u = p[i - 1]; // previous alarm
            int v = p[i];     // next alarm
            
            current_time += distAlarm[u][room[v]] + a[v];
            
            if (current_time > d[v]) {
                possible = false;
            }
        }

        // If this entire permutation is valid, minimize the answer
        if (possible) {
            ans = min(ans, current_time);
        }

    } while (next_permutation(p.begin(), p.end()));

    if (ans == INF) cout << "IMPOSSIBLE\n";
    else cout << ans << "\n";

    return 0;
}

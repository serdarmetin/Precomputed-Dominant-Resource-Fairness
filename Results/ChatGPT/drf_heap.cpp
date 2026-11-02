#include <cstdint>
#include <queue>
#include <vector>

struct Node {
    double share;
    double neg_ds;
    int index;
    std::uint64_t version;
};
struct Greater {
    bool operator()(const Node& a, const Node& b) const {
        if (a.share != b.share) return a.share > b.share;
        if (a.neg_ds != b.neg_ds) return a.neg_ds > b.neg_ds;
        if (a.index != b.index) return a.index > b.index;
        return a.version > b.version;
    }
};

extern "C" void drf_heap_run(const std::int64_t* demands, const std::int64_t* reserves,
                              const double* ds, int n, int m,
                              std::int64_t* counts, std::int64_t* consumed) {
    std::vector<double> shares(n, 0.0);
    std::vector<std::uint64_t> versions(n, 0);
    for (int i = 0; i < n; ++i) counts[i] = 0;
    for (int j = 0; j < m; ++j) consumed[j] = 0;
    std::priority_queue<Node, std::vector<Node>, Greater> heap;
    for (int i = 0; i < n; ++i) heap.push(Node{0.0, -ds[i], i, 0});

    while (!heap.empty()) {
        Node cur = heap.top(); heap.pop();
        int i = cur.index;
        if (cur.version != versions[i]) continue;
        bool infeasible = false;
        for (int j = 0; j < m; ++j) {
            if (reserves[j] < consumed[j] + demands[i*m + j]) {
                infeasible = true;
                break;
            }
        }
        if (infeasible) break;
        ++counts[i];
        for (int j = 0; j < m; ++j) consumed[j] += demands[i*m + j];
        shares[i] += ds[i];
        ++versions[i];
        heap.push(Node{shares[i], -ds[i], i, versions[i]});
    }
}

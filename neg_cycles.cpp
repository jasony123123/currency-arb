#include <bits/stdc++.h>
using namespace std;

#define Edge pair<pair<int, int>, pair<long double, int>>
#define v_src first.first
#define v_end first.second
#define e_cost second.first
#define e_id second.second

#define Pred pair<int, int>
#define p_vertex first
#define p_eid second

#define NULL_VERTEX -1
#define NULL_PRED pair<int, int>(-1, -1)

pair<long double, string> extract_path(int num_ver, int relaxed_v,
                                       vector<Pred> &pred,
                                       vector<long double> &idToCost) {
  vector<bool> seen(num_ver, false);
  vector<Pred> path;
  string ret = "";
  long double totalCost = 0;

  for (int j = relaxed_v;; j = pred[j].p_vertex) {
    if (seen[j]) {
      do {
        ret += to_string(path.back().p_vertex) + " " +
               to_string(path.back().p_eid) + " ";
        totalCost += idToCost[path.back().p_eid];
        path.pop_back();
      } while (path.size() > 0 && path.back().p_vertex != j);
      break;
    }
    seen[j] = true;
    path.push_back(pred[j]);
  }

  return {totalCost, ret};
}

void bellman_ford(int num_ver, vector<Edge> &edge_list) {
  vector<long double> dist(num_ver, 0);
  vector<Pred> pred(num_ver, NULL_PRED);

  for (int i = 1; i <= num_ver + 1; i++) {
    int relaxed_v = NULL_VERTEX;
    vector<int> wasRelaxed;

    for (Edge e : edge_list) {
      long double relaxed_cost = dist[e.v_src] + e.e_cost;
      if (dist[e.v_end] > relaxed_cost + 1e-7) {
        dist[e.v_end] = relaxed_cost;
        pred[e.v_end] = {e.v_src, e.e_id};
        relaxed_v = e.v_end;
        wasRelaxed.push_back(e.v_end);
      }
    }

    if (relaxed_v == NULL_VERTEX) {
      puts(" |No");
      break;
    }
    if (i == num_ver + 1) {
      printf(" |Yes ");
      vector<long double> idToCost(edge_list.size(), 0);
      for(Edge e : edge_list)
        idToCost[e.e_id] = e.e_cost;

      vector<pair<long double, string>> all_cycles;
      for(int vv : wasRelaxed)
        all_cycles.push_back(extract_path(num_ver, vv, pred, idToCost));

      sort(all_cycles.begin(), all_cycles.end());
      cout << all_cycles[0].second << "\n";
    }
  }
}

int main() {
  int num_ed, num_ve;
  vector<Edge> e_list;
  cin >> num_ed >> num_ve;
  while (num_ed--) {
    Edge e;
    cin >> e.v_src >> e.v_end >> e.e_cost >> e.e_id;
    e_list.push_back(e);
  }
  bellman_ford(num_ve, e_list);
  return 0;
}

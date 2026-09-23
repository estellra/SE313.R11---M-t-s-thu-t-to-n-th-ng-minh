// Sinh chỉnh hợp chập m của n phần tử

#include <iostream>
#include <vector>

using namespace std;

int n, m;
int a[100];
bool is_last = false;

void init() {
    for (int i = 1; i <= m; i++) {
        a[i] = i;
    }
}

void next_arrangement(){
    int i = m;

    while(i >= 1){
        vector<bool> used(n + 1, false);
        for(int j = 1; j < i; j++){
            used[a[j]] = true;
        }

        for(int v = a[i] + 1; v <= n; v++){
            if(!used[v]){
                a[i] = v;
                used[a[i]] = true;

                int cur = 1;
                for(int j = i + 1; j <= m; j++){
                    while(used[cur]) cur++;
                    a[j] = cur;
                    used[cur] = true;
                }

                return;
            }
        }
        i--;
    }

    is_last = true;
}

int main() {
    cin >> n >> m;
    if(m < 1 || m > n || n > 99) return 0;
    init();
    is_last = false;

    while(!is_last){
        for(int i = 1; i <= m; i++){
            cout << a[i] << " ";
        }
        cout << endl;
        next_arrangement();
    }

    return 0;
}
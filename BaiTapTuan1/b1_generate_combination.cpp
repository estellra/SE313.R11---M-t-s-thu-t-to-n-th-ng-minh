// Sinh tổ hợp chập k của n phần tử

#include <iostream>

using namespace std;

int n, k, a[100];
bool is_last;

void init(){
    for(int i = 1; i <= k; i++){
        a[i] = i;
    }
}

void next_combination(){
    int i = k;

    while(i >= 1 && a[i] == n - k + i){
        i--;
    }

    if(i < 1) {
        is_last = true;
        return;
    }
    
    a[i]++;

    for(int j = i + 1; j <= k; j++){
        a[j] = a[j - 1] + 1;
    }

}

int main(){
    cin >> n >> k;
    if(k < 1 || k > n || n > 99) return 0;

    init();
    
    is_last = false;
    while(!is_last){
        for(int i = 1; i <= k; i++){
            cout << a[i] << " ";
        }
        cout << endl;
        next_combination();
    }

    return 0;
}
// Sinh dãy nhị phân n -bit

#include <iostream>

using namespace std;

int n, a[100];
bool is_last;

void init(){
    for(int i = 0; i < n; i++){
        a[i] = 0;
    }    
}

void next_binary(){
    int i = n - 1;
    while(i >= 0 && a[i] == 1){
        a[i] = 0; 
        --i;
    }

    if(i < 0) is_last = true;
    else a[i] = 1;
}

int main(){
    cin >> n;
    if(n < 1 || n > 100) return 0;
    is_last = false;
    init();
    while(!is_last){
        for(int i = 0; i < n; i++){
            cout << a[i];
        }
        cout << endl;
        next_binary();
    }

    return 0;
}
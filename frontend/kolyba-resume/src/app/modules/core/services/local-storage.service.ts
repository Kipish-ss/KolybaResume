import { Auth, onAuthStateChanged } from '@angular/fire/auth';
import { accessTokenLocalStorage, emailVerifiedLocalStorage, userLocalStorage } from '@core/constants/local-storage.constants';

import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class LocalStorageService {
    public constructor(
        private readonly auth: Auth,
        authStoreService: AuthStoreService,
    ) {
        onAuthStateChanged(this.auth, (user) => {
            if (user) {
                user.getIdToken().then((t) => authStoreService.setAccessToken(t));
                authStoreService.setEmailVerified(user.emailVerified);
            }
        });

        authStoreService.setAccessToken(localStorage.getItem(accessTokenLocalStorage) ?? '');
        if (localStorage.getItem(emailVerifiedLocalStorage)) {
            authStoreService.setEmailVerified(JSON.parse(localStorage.getItem(emailVerifiedLocalStorage)!));
        }

        if (localStorage.getItem(userLocalStorage)) {
            authStoreService.setUser(JSON.parse(localStorage.getItem(userLocalStorage)!));
        }
    }
}

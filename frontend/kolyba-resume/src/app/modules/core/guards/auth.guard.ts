import { CanActivate, Router, UrlTree } from '@angular/router';
import { Observable, map } from 'rxjs';

import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { Injectable } from '@angular/core';

@Injectable({
    providedIn: 'root',
})
export class AuthGuard implements CanActivate {
    // eslint-disable-next-line no-empty-function
    constructor(private authStoreService: AuthStoreService, private router: Router) {}

    canActivate(): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
        return this.authStoreService.emailVerified$.pipe(
            map(emailVerified => emailVerified ? true : this.router.parseUrl('/auth/signIn'))
        )
    }
}

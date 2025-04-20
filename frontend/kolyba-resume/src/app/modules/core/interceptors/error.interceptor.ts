import { catchError, switchMap, throwError } from 'rxjs';

import { AuthService } from '@auth//services/auth.service';
import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';

export const errorInterceptorFn: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const authStoreService = inject(AuthStoreService);

  const handleError = (error: any) => {
    return throwError(() => new Error(error?.message ?? 'Something went wrong'));
  };

  const handleExpired = () => {
    return authStoreService.accessToken$.pipe(
      switchMap((token) => {
        const clonedReq = req.clone({
          setHeaders: {
            Authorization: `Bearer ${token}`,
          },
        });
        return next(clonedReq);
      })
    );
  };

  return next(req).pipe(
    catchError((errorResponse) => {
      if (errorResponse.status === 401) {
        return authService.refreshToken().pipe(
          switchMap(() => handleExpired())
        );
      }

      return handleError(errorResponse);
    })
  );
};

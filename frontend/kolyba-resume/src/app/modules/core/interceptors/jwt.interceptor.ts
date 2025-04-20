import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { switchMap } from 'rxjs';

export const jwtInterceptorFn: HttpInterceptorFn = (req, next) => {
  const authStoreService = inject(AuthStoreService);

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

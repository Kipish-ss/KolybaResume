import { BehaviorSubject } from 'rxjs';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class SpinnerService {
    private isLoading$$ = new BehaviorSubject<boolean>(false);

    public readonly isLoading$ = this.isLoading$$.asObservable();

    public show(): void {
        this.isLoading$$.next(true);
    }

    public hide(): void {
        this.isLoading$$.next(false);
    }
}

import { NavigationCancel, NavigationEnd, NavigationError, NavigationStart, Router, RouterOutlet } from '@angular/router';

import { Component } from '@angular/core';
import { LoadingSpinnerComponent } from '@core/components/loading-spinner/loading-spinner.component';
import { LocalStorageService } from '@core/services/local-storage.service';
import { SpinnerService } from './modules/core/services/spinner.service';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, LoadingSpinnerComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.scss'
})
export class AppComponent {
    constructor(private router: Router, private spinner: SpinnerService, private readonly localStorageService: LocalStorageService) {
        this.listenRouter();
    }

    private listenRouter() {
        this.router.events.subscribe((event) => {
            if (event instanceof NavigationStart) {
                this.spinner.show();
            }
            if (
                event instanceof NavigationEnd ||
                event instanceof NavigationCancel ||
                event instanceof NavigationError
            ) {
                this.spinner.hide();
            }
        });
    }
}

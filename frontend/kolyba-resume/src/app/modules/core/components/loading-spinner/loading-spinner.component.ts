import { Component, Input } from '@angular/core';

import { CommonModule } from '@angular/common';
import { SpinnerService } from '@core/services/spinner.service';

@Component({
    selector: 'kr-loading-spinner',
    imports: [
        CommonModule
    ],
    templateUrl: './loading-spinner.component.html',
})
export class LoadingSpinnerComponent {
    // eslint-disable-next-line no-empty-function
    constructor(public spinnerService: SpinnerService) {}

    @Input() overlay: boolean = false;

    @Input() size = '20px';

    @Input() top = '30%';

    @Input() left = '49%';

    @Input() position = 'absolute';

    @Input() margin = '100px auto';
}

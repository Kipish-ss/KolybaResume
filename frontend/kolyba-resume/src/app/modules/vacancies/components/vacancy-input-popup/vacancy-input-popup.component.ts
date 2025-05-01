import { FormControl, Validators } from '@angular/forms';

import { Component } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { VacanciesStoreService } from '../../store/services/vacancies-store.service';

@Component({
    selector: 'app-vacancy-input-popup',
    standalone: false,
    templateUrl: './vacancy-input-popup.component.html',
    styleUrl: './vacancy-input-popup.component.scss'
})
export class VacancyInputPopupComponent {
    public readonly urlControl = new FormControl('', Validators.pattern('https?://.+'));
    public readonly descControl = new FormControl('');

    constructor(
        private dialogRef: MatDialogRef<VacancyInputPopupComponent>,
        private vacanciesStoreService: VacanciesStoreService
    ) { }

    public loadByUrl(): void {
        if (this.urlControl.valid) {
            this.vacanciesStoreService.loadJobDescription(this.urlControl.value!);
        }
    }

    public submit(): void {
        const desc = this.descControl.value;
        if (desc) {
            this.dialogRef.close();
        }
    }

    public close(): void {
        this.dialogRef.close();
    }
}

import { AuthStoreService } from '@auth//store/services/auth-store.service';
import { Component } from '@angular/core';

@Component({
    selector: 'kr-upload-resume',
    standalone: false,
    templateUrl: './upload-resume.component.html',
    styleUrl: './upload-resume.component.scss'
})
export class UploadResumeComponent {
    constructor(private authStoreService: AuthStoreService) { }

    onFileSelected(event: Event): void {
        const input = event.target as HTMLInputElement;
        if (input.files && input.files.length) {
            const file = input.files[0];
            this.authStoreService.uploadResume(file);
        }
    }
}


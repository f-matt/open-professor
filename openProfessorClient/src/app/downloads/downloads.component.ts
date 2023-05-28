import { Component } from '@angular/core';
import { QuestionsService } from '../services/questions.service';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-downloads',
  templateUrl: './downloads.component.html',
  styleUrls: ['./downloads.component.css']
})
export class DownloadsComponent {

  constructor(private questionsService : QuestionsService) {}

  download() {
		this.questionsService.downloadFile().subscribe((response: any) => {
			let blob:any = new Blob([response], { type: 'text/json; charset=utf-8' });
			const url = window.URL.createObjectURL(blob);
			//window.open(url);
			saveAs(blob, 'file.xml');
			}), (error: any) => console.log('Error downloading the file'),
			() => console.info('File downloaded successfully');
	}

}

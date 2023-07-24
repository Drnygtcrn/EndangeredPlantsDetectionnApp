import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TukenmektelerComponent } from './tukenmekteler.component';

describe('TukenmektelerComponent', () => {
  let component: TukenmektelerComponent;
  let fixture: ComponentFixture<TukenmektelerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TukenmektelerComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TukenmektelerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

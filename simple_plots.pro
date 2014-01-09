pro simple_plots

set_plot,'X'
plotstuff,/set,/silent
!p.font=0
loadct,39

; all AAS registrants

set_plot,'ps'

device,filename='all_ppl.eps',/encap,/color
barplot,[0.66,0.34]*100.,xlabels=['!7Male','!7Female'],ytitle='% of People',title='All AAS 223 Registrants',yrange=[0,100]
device,/close



;-- make simple plots based on #'s from Alex
device,filename='all_speaker.eps',/encap,/color
barplot,[65.1,34.9],xlabels=['!7Male','!7Female'],ytitle='% of People',title='Total Speakers',yrange=[0,100]
device,/close

device,filename='all_questions.eps',/encap,/color
barplot,[75.4, 24.6],xlabels=['!7Male','!7Female'],ytitle='% of People',title='Total Questions',yrange=[0,100]
device,/close


device,filename='first_questions.eps',/encap,/color
barplot,[75.5, 24.5],xlabels=['!7Male','!7Female'],ytitle='% of People',title='First Questions',yrange=[0,100]
device,/close


device,filename='one_question.eps',/encap,/color
barplot,[67.4, 32.6],xlabels=['!7Male','!7Female'],ytitle='% of People',title='Only One Question',yrange=[0,100]
device,/close


device,filename='2gram.eps',/encap,/color
plot,[1,2,3,4],[230,82,91,23],thick=5,xtickname=['MM','MF','FM','FF'],charsize=1.3
oplot,[1,2,3,4],[243,79,79,25],linestyle=2,thick=5,color=55
device,/close

device,filename='3gram.eps',/encap,/color
plot,findgen(8),[79,30,45,41,10,18,11,6],thick=5,xtickname=['MMM','MMF','MFM','FMM','MFF','FMF','FFM','FFF'],xticks=7,xtickv=findgen(10),charsize=1.3
oplot,findgen(8),[103,33,33,33,11,11,11,4],linestyle=2,thick=5,color=55
device,/close



set_plot,'X'
stop
end

pro findgender,infile
; written in IDL, because I am stupid and old and lazy

if not keyword_set(infile) then infile = 'aas_registrant_firstname.txt'

readcol,infile,aas_name,f='(A)',/silent
readcol,'female_uniq.csv',f_name,f_num,f='(A,F)',/silent
readcol,'male_uniq.csv',m_name,m_num,f='(A,F)',/silent


f_name = strlowcase(f_name)
m_name = strlowcase(m_name)
aas_name = strlowcase(aas_name)

gender = strarr(n_elements(aas_name)) + 'x'

for n=0L,n_elements(aas_name)-1 do begin
   xf = where(f_name eq aas_name[n])
   xm = where(m_name eq aas_name[n])

   if xf[0] eq -1 and xm[0] eq -1 then continue

   if xm[0] ne -1 and xf[0] ne -1 then begin
      g = f_num[xf[0]] / m_num[xm[0]]
      if g gt 1. then gender[n] = 'f'
      if g le 1. then gender[n] = 'm'
   endif

   if xm[0] ne -1 and xf[0] eq -1 then gender[n] = 'm'
   if xf[0] ne -1 and xm[0] eq -1 then gender[n] = 'f'

endfor

forprint,textout=infile+'.gender',aas_name,gender,/silent,/nocomm,f='(A,",",A4)'





print,''
print,'fraction of names w/ gender assigned:'
print,float(n_elements(where(gender ne "x")))/float(n_elements(gender))


print,''
print,'fraction of men'
print,float(n_elements(where(gender eq "m")))/float(n_elements(where(gender ne "x")))


print,''
print,'fraction of women'
print,float(n_elements(where(gender eq "f")))/float(n_elements(where(gender ne "x")))




stop
end

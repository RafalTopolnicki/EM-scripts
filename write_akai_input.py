def scf_input(filename, elements, concentrations, symmetry, lattice_constant, ew, xc, rel,
              bzqlty, pmix, edelt, mxl):
    comment_line = 'c-------------------------\n'
    rmt = 0
    with open(filename+'.inp', 'w') as file:
        file.write(f'c--- elements {elements}\n')
        file.write(f'{comment_line}')
        file.write(f'go {filename}.pot\n')
        file.write(f'{comment_line}')
        file.write(f'c   brvtyp     a        c/a   b/a   alpha   beta   gamma\n')
        file.write(f'   {symmetry}  {lattice_constant:.3f} ,    ,   ,   ,   ,   ,\n')
        file.write(f'{comment_line}')
        file.write(f'c   edelt    ewidth    reltyp   sdftyp   magtyp   record\n')
        file.write(f'    {edelt}    {ew}    {rel}   {xc}      nmag      init\n')
        file.write(f'{comment_line}')
        file.write(f'c   outtyp    bzqlty   maxitr   pmix\n')
        file.write(f'    update     {int(bzqlty)}    500 {pmix}\n')
        file.write(f'{comment_line}')
        file.write(f'c  ntyp\n')
        file.write(f'   1\n')
        file.write(f'{comment_line}')
        file.write(f'c   type    ncmp    rmt    field   mxl  anclr   conc\n')
        file.write(f'   X   {len(elements)}  {rmt}  {0.0}   {mxl}\n')
        for element, concentration in zip(elements, concentrations):
            file.write(f'       {element}   {concentration}\n')
        file.write(f'{comment_line}')
        file.write(f'c natm\n')
        file.write(f'   1\n')
        file.write(f'{comment_line}')
        file.write(f'c   atmicx                        atmtyp\n')
        file.write(f'0a         0b         0c       X\n')
        file.write(f'{comment_line}')
        file.close()
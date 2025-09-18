" random bs
set nocompatible
set ignorecase
set incsearch
set tabstop=4
set shiftwidth=4
set expandtab
let mapleader = " "
let g:netrw_banner = 0

" random bs I really care about
filetype plugin indent on
syntax on
set relativenumber
set cursorline

colorscheme slate

" workflow shit
inoremap jk <Esc>
inoremap kj <Esc>
noremap <leader>nvim :e C:\Users\gerfr\AppData\Local\nvim\init.vim<CR>
noremap <leader>c :w<CR>:silent !powershell "pdflatex %"<CR>
noremap <leader>C :w<CR>:!powershell "pdflatex %"<CR>
noremap <leader>e :Explore<CR>
noremap <leader>s :w<CR>:source %<CR>
vnoremap <leader>y "+y
noremap <leader>p "+p
 
"pannel navigation (regularly with <C-w>)
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

nnoremap <leader>V <C-w>v
nnoremap <leader>S <C-w>s

nnoremap <leader>H <C-w>H
nnoremap <leader>J <C-w>J
nnoremap <leader>K <C-w>K
nnoremap <leader>L <C-w>L
nnoremap <leader>T <C-w>T

"tab navigation (gt -> next tab; gT -> previous tab)
nnoremap <leader>t :tabnew<CR>
nnoremap <leader>1 1gt
nnoremap <leader>2 2gt
nnoremap <leader>3 3gt
nnoremap <leader>4 4gt
nnoremap <leader>5 5gt
nnoremap <leader>6 6gt
nnoremap <leader>7 7gt
nnoremap <leader>8 8gt
nnoremap <leader>9 9gt

" Todo Binds
noremap <leader>d 0ax<Esc>ddGpgg

function! NewTask()
    call inputsave()
    let l:target = input("Task: ")
    call inputrestore()
    execute "normal! o[] " . l:target
endfunction

noremap <leader>n :call NewTask()<CR>

" LaTex Binds
function! LatexNew()
    call inputsave()
    let l:inp = input("Name: ")
    call inputrestore()
    execute "normal! o\\begin{" . l:inp
    execute "normal! a}\n\\end{" . l:inp
    execute "normal! a}"
    execute "normal! Otemp"
endfunction

noremap <leader>l :call LatexNew()<CR>

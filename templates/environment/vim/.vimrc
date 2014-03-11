" Referenced here: http://vimuniversity.com/samples/your-first-vimrc-should-be-nearly-empty
" Most added from: http://stevelosh.com/blog/2010/09/coming-home-to-vim/
" Python http://sontek.net/turning-vim-into-a-modern-python-ide
" & http://dancingpenguinsoflight.com/2009/02/python-and-vim-make-your-own-ide/
" If you don't understand a setting in here, just type ':h setting'.

" Use Vim settings, rather than Vi settings (much better!).
set nocompatible

" Pathogen plugin manager
" filetype off
" call pathogen#infect()
" call pathogen#helptags()

" Set 256 colors
let &t_Co=256

" remap the leader
let mapleader = ","
" ; is equal to :
nnoremap ; :

" Make backspace behave in a sane manner.
set backspace=indent,eol,start

" Switch syntax highlighting on
syntax on

" Try to detect filetypes
filetype on

" Enable file type detection and do language-dependent indenting.
filetype plugin indent on

" Tab setting. See: http://vimcasts.org/episodes/tabs-and-spaces/
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab

" Sanity options
set encoding=utf-8
set scrolloff=5
set autoindent
" To not autoident pasted text
set pastetoggle=<F2>
set showmode
set showcmd
set hidden
set wildmenu
set wildmode=list:longest
set visualbell
set cursorline
set ttyfast
set ruler
set backspace=indent,eol,start
set laststatus=2
" Always show line numbers, but only in current window.
set number
au WinEnter * :setlocal number
au WinLeave * :setlocal nonumber

" Search options
" 1st two line make perl/python like regex searches
nnoremap / /\v
vnoremap / /\v
set ignorecase
set smartcase
" global replace
set gdefault
set incsearch
set showmatch
set hlsearch
" ,<space> to remove search hightlighting
nnoremap <leader><space> :noh<cr>
" match brackets
nnoremap <tab> %
vnoremap <tab> %

" Wrapping options/columns width
set wrap
set textwidth=79
set formatoptions=qrn1
if exists('+colorcolumn')
      set colorcolumn=80
else
      au BufWinEnter * let w:m2=matchadd('ErrorMsg', '\%>80v.\+', -1)
endif

" Show invisible chars
set list
set listchars=tab:▸\ ,eol:¬

" autosave when focus lost on terminal
au FocusLost * :wa

" Misc
" Opened a read-only file then :w!! lets you save it
cmap w!! %!sudo tee > /dev/null %

" Return the cursor to the line you were on the last time you were editing that
if has("autocmd")
    autocmd BufReadPost * if line("'\"") > 0 && line ("'\"") <= line("$") | exe "normal! g'\"" | endif
  endif

" No bells. No flashing screen.
set visualbell
set t_vb=
au GUIEnter * set t_vb=

" Toggle line numbers and fold column for easy copying:
nnoremap <F3> :set nonumber!<CR>:set foldcolumn=0<CR>

" ColorScheme
" For solarized
" let g:solarized_termcolors=256
" set background=dark
" colorscheme solarized
" Gardener cs
" set background=dark
colorscheme molokai
" this setting MUST be set here. If not, background 
" and comments will have the same color
" set background=dark

" For powerline plugin
"let Powerline_symbols = 'unicode'

" For indent guides plugin
"let g:indent_guides_auto_colors = 0
"autocmd VimEnter,Colorscheme * :hi IndentGuidesOdd ctermbg=236
"autocmd VimEnter,Colorscheme * :hi IndentGuidesEven ctermbg=232
"let g:indent_guides_start_level = 2
"let g:indent_guides_guide_size = 1
"au VimEnter * :IndentGuidesEnable

" For Pydiction
"let g:pydiction_location = 'bundle/Pydiction/complete-dict'

" Improved Python syntax highlighting
"autocmd FileType python set complete+=k~/.vim/syntax/python.vim isk+=.,(

" Execute file being edited with <Shift> + e:
map <buffer <S-e> :w<CR>:!/usr/bin/env python % <CR>


" For tagbar
nnoremap <silent> <F4> :TagbarToggle <CR>

let g:syntastic_python_checker = 'pyflakes'

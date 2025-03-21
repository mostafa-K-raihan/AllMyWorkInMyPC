-- Make sure to setup `mapleader` and `maplocalleader` before
-- loading lazy.nvim so that mappings are correct.
-- This is also a good place to setup other settings (vim.opt)
vim.g.mapleader = " "
vim.g.maplocalleader = "\\"


-- tab / space stuff
vim.cmd('set tabstop=2') -- Sets tab width to 2 spaces.
vim.cmd('set softtabstop=2') -- Makes tab/backspace behave as 2 spaces.
vim.cmd('set shiftwidth=2') -- Sets indentation width to 2 spaces.
vim.cmd('set expandtab') -- Expands tabs to spaces.
-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)


-- Setup lazy.nvim
require("lazy").setup({
  spec = {
    -- add your plugins here
    { "catppuccin/nvim", name = "catppuccin", priority = 1000 },
    { "nvim-telescope/telescope.nvim", tag = "0.1.8", dependencies = { 'nvim-lua/plenary.nvim' } }
  },
  -- Configure any other settings here. See the documentation for more details.
  -- colorscheme that will be used when installing plugins.
  install = { colorscheme = { "habamax" } },
  -- automatically check for plugin updates
  checker = { enabled = true },
})

local builtin = require('telescope.builtin')

vim.keymap.set('n', '<C-p>', builtin.find_files, {})
vim.keymap.set('n', '<leader>/', builtin.live_grep, {})


require("catppuccin").setup()
vim.cmd.colorscheme "catppuccin"

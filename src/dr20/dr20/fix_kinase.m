function out = fix_kinase(kinase)
out = regexprep(regexprep(kinase, '_+$', ''), ...
                '_+pg_cell$', '');
end

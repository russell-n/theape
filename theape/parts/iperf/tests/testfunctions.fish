function configspecfeature
    cd ../
    tangleweave iperfsettings.pnw
    cd tests/steps
    tangleweave configspecfeature.pnw
    cd ../
    behave features/configspec.feature
end

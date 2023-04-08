#!/bin/bash

declare -a parts

usage() {
    echo "usage: $0: <jlc-parts-file> <library name> [patches dir]"
    echo
    echo "parts file:       one Cxxxxx per line, # comments allowed"
    echo "library name:     A-Z0-9 in both filesystem and KiCad"
    echo "patches dir:      directory of patches to apply to footprints (optional)"
}

read_parts_file() {

    while read line; do
        local part=$(echo $line | sed -ne 's/^\(C[0-9]*\) .*$/\1/p')
        parts+=($part)
    done < $jlc_parts_file
}

function apply_patches_if_needed() {
    library_name=$1
    patches_dir=$2

    if [[ ! -d $library_name/$library_name ]]; then
        echo "apply_patches_if_needed(): no footprints found!"
        return 1
    fi

    if [[ ! -d $patches_dir ]]; then
        echo "No patches to apply"
        return 0
    fi

    echo "Applying patches:"
    for file in $patches_dir/*.patch; do
        footprint_name=$(basename $(echo $file | sed -e 's/.patch//g'))
        echo -n "* "
        patch $library_name/$library_name/$footprint_name < $file
    done

}

fix_smd_attr() {
    library_name=$1

    if [[ ! -d $library_name/$library_name ]]; then
        echo "fix_smd_attr(): no footprints found!"
        return 1
    fi

    echo "Processing footprints:"
    for file in $library_name/$library_name/*.kicad_mod; do
        echo -n "* $(basename $(basename $file)): "

        # not for us
        grep 'pad.*thru_hole' $file > /dev/null
        if [[ $? == 0 ]]; then
            echo "THT"
            continue
        fi

        # adjusted?
        grep "attr smd" $file > /dev/null
        if [[ $? == 1 ]]; then
            echo "SMD (patching)"
            sed -ie 's/^\((module.*$\)/\1\n  (attr smd)/g' $file
        else
            echo "SMD"
        fi
    done
}

main() {
    if [[ "$2" == "" ]]; then
        usage
        exit 0
    fi

    local jlc_parts_file=$1
    local library_name=$2
    local patches_dir=$3

    if [[ ! -f "$jlc_parts_file" ]]; then
        usage
        exit 0
    fi

    library_name_no_space=$(echo $library_name | sed 's/ /-/g')
    #echo "library name: $library_name, library_name no space: $library_name_no_space"
    if [[ "$library_name_no_space" != "$library_name" ]]; then
        echo "error: space(s) in library name not allowed."
        exit 1
    fi

    library_name_work=${library_name}-work

    read_parts_file $jlc_parts_file

    echo "Downloading components:"
    # --skip_existing: always overwrite!
    JLC2KiCadLib ${parts[*]} \
        -dir ${library_name} \
        -schematic_lib $library_name -footprint_lib $library_name | 
        grep --line-buffered -v '\(creating footprint\|creating 3D model\|writing in\)' | 
        sed -ne 's/.*INFO - \(.*\)$/\1/p'

    echo

    fix_smd_attr $library_name
    echo
    apply_patches_if_needed $library_name $patches_dir
}

main $*


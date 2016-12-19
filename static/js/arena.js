/**
 * Created by lahim on 12/16/16.
 */

function loadMap() {
    $.get("http://localhost:8000/arena", function (arena) {
        renderMap(arena.map);
        renderBots(arena.bots);
        renderBombs(arena.bombs);
    });
}

function renderBots(bots) {
    $.each(bots, function (idx, bot) {
        var tileId = "#tile_" + bot.location[0] + "_" + bot.location[1];
        $(tileId).addClass("bot");

        if (idx % 2 == 0) {
            $(tileId).addClass("bot-red");
        } else {
            $(tileId).addClass("bot-blue");
        }
    });
}

function renderBombs(bombs) {
    $.each(bombs, function (idx, bomb) {
        $("#tile_" + bomb.location[0] + "_" + bomb.location[1]).addClass("tile-boom");
        $.each(bomb.destruction, function (i, loc) {
            var tileId = "#tile_" + loc[0] + "_" + loc[1];

            if (bomb.tte == 0) {
                $(tileId).addClass("tile-boom-exp");
            } else if (bomb.tte == -1) {
                $(tileId).removeClass("tile-boom-exp").removeClass("tile-boom");
            }
        });
    });
}

window.setInterval(function () {
    loadMap();
}, 1000);

function renderMap(map) {
    // var arenaHtml = $('#arena-map').html();

    var template = "";

    $.each(map, function (row, rowElement) {
        template += '<div class="arena-row">';
        $.each(rowElement, function (col, colElement) {
            template += '<div id="tile_' + col + '_' + row + '" class="arena-col tile-' + colElement + '">';
            template += '&nbsp';
            template += '</div>';
        });
        template += '</div>';
    });
    // Mustache.parse(template);   // optional, speeds up future uses
    // var rendered = Mustache.render(template, {map: map});
    $('#arena').html(template);
    // $('#arena').load();
}

$(document).ready(function () {
});

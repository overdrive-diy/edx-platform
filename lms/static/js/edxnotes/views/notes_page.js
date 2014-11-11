;(function (define, undefined) {
    'use strict';
    define([
        'jquery', 'underscore', 'backbone', 'js/edxnotes/collections/notes',
        'js/edxnotes/views/note_item', 'js/edxnotes/utils/logger'
    ], function ($, _, Backbone, NotesCollection, NoteItemView, Logger) {
        var NotesPageView = Backbone.View.extend({
            className: 'edxnotes-page-wrapper',
            initialize: function (options) { },
            render: function () {
                var items, context;

                items = this.collection.map(function(model) {
                    return (new NoteItemView({model: model})).render().$el;
                });
                context = $.extend(true, {});
                this.$el.append.apply(this.$el, items);
                return this;
            }
        });

        return function (container, notesList) {
            var collection = new NotesCollection(notesList, {parse: true}),
                view = new NotesPageView({
                    collection: collection
                }).render();
            $(container).empty().append(view.$el);
        };
    });
}).call(this, define || RequireJS.define);
